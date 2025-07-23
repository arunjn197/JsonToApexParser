import json
import keyword
import argparse

APEX_KEYWORDS = {
    "abstract", "activate", "and", "any", "array", "as", "asc", "autonomous", "begin", "bigdecimal", "blob", "boolean",
    "break", "bulk", "by", "byte", "case", "cast", "catch", "char", "class", "collect", "commit", "const", "continue",
    "convertcurrency", "date", "datetime", "decimal", "default", "delete", "desc", "do", "else", "end", "enum", "exception",
    "exit", "export", "extends", "false", "final", "finally", "float", "for", "from", "future", "global", "goto", "group",
    "having", "if", "implements", "import", "inner", "insert", "instanceof", "int", "interface", "into", "join", "like",
    "limit", "list", "long", "loop", "map", "merge", "new", "not", "null", "nulls", "number", "object", "of", "on", "or",
    "outer", "override", "package", "parallel", "pragma", "private", "protected", "public", "retrieve", "return", "rollback",
    "select", "set", "short", "static", "super", "switch", "synchronized", "system", "testmethod", "then", "this", "throw",
    "time", "transaction", "transient", "trigger", "true", "try", "undelete", "update", "upsert", "using", "virtual", "void",
    "webservice", "when", "where", "while", "with", "without"
}

def to_camel_case(s):
    parts = s.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

def is_apex_keyword(word):
    return word.lower() in APEX_KEYWORDS

def safe_field_name(json_key):
    camel = to_camel_case(json_key)
    if is_apex_keyword(camel) or not camel.isidentifier():
        return f'_{camel}'
    return camel

def infer_apex_type(value):
    if isinstance(value, str):
        return 'String'
    elif isinstance(value, bool):
        return 'Boolean'
    elif isinstance(value, int):
        return 'Integer'
    elif isinstance(value, float):
        return 'Decimal'
    elif isinstance(value, list):
        if len(value) > 0:
            return f'List<{infer_apex_type(value[0])}>'
        else:
            return 'List<Object>'
    elif isinstance(value, dict):
        return 'Object'
    else:
        return 'Object'

def generate_apex_class(name, json_data, indent=0, is_root=False):
    fields = []
    inner_classes = []
    indent_str = '    ' * indent
    class_name = name[0].upper() + to_camel_case(name[1:])

    fields.append(f'{indent_str}public class {class_name} ' + '{')

    for key, value in json_data.items():
        field_name = safe_field_name(key)
        comment = f' // "{key}" -> {field_name}' if field_name != to_camel_case(key) else ''

        if isinstance(value, dict):
            nested_class_name = key[0].upper() + to_camel_case(key[1:])
            fields.append(f'{indent_str}    public {nested_class_name} {field_name};{comment}')
            nested_code = generate_apex_class(key, value, indent + 1)
            inner_classes.append(nested_code)
        elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
            nested_class_name = key[0].upper() + to_camel_case(key[1:])
            fields.append(f'{indent_str}    public List<{nested_class_name}> {field_name};{comment}')
            nested_code = generate_apex_class(key, value[0], indent + 1)
            inner_classes.append(nested_code)
        else:
            apex_type = infer_apex_type(value)
            fields.append(f'{indent_str}    public {apex_type} {field_name};{comment}')

    if is_root:
        fields.append('')
        fields.append(f'{indent_str}    public static {class_name} fromJSON(String json) {{')
        fields.append(f'{indent_str}        return ({class_name}) JSON.deserialize(json, {class_name}.class);')
        fields.append(f'{indent_str}    }}')
        fields.append('')
        fields.append(f'{indent_str}    public String toJSON() {{')
        fields.append(f'{indent_str}        return JSON.serialize(this);')
        fields.append(f'{indent_str}    }}')

    fields.extend(inner_classes)
    fields.append(f'{indent_str}}}')
    return '\n'.join(fields)


def convert_json_to_apex(json_data, root_class_name="Root"):
    if isinstance(json_data, dict):
        return generate_apex_class(root_class_name, json_data, indent=0, is_root=True)
    elif isinstance(json_data, list) and len(json_data) > 0 and isinstance(json_data[0], dict):
        return generate_apex_class(root_class_name, json_data[0], indent=0, is_root=True)
    else:
        raise ValueError("JSON must be an object or a list of objects.")

def main():
    parser = argparse.ArgumentParser(description='Convert JSON to Apex class')
    parser.add_argument('input', help='Path to input JSON file')
    parser.add_argument('-o', '--output', help='Path to output Apex .cls file')
    parser.add_argument('-c', '--classname', default='Root', help='Root Apex class name')

    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        json_str = f.read()
        json_data = json.loads(json_str)

    apex_code = convert_json_to_apex(json_data, root_class_name=args.classname)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(apex_code)
        print(f'Apex class written to {args.output}')
    else:
        print(apex_code)

if __name__ == '__main__':
    main()
