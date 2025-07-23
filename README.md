# 🔁 json2apex — Convert JSON to Apex Classes

**json2apex** is a Python-based CLI tool that converts any JSON structure into valid Apex classes — complete with wrapper class design, nested inner classes, safe field names, and bidirectional serialization (`fromJSON()` and `toJSON()`).

---

## 🚀 Features

- ✅ Converts JSON to Apex class with nested `public class` wrappers
- ✅ Escapes Apex reserved keywords safely (e.g., `public`, `class`, `return`)
- ✅ Generates `fromJSON()` and `toJSON()` methods for easy serialization
- ✅ Creates `*.cls-meta.xml` for Salesforce deployment
- ✅ Supports nested objects and arrays
- ✅ CLI-ready for terminal use

---

## 📦 Installation

```bash
git clone https://github.com/your-username/json2apex.git
cd json2apex
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # (empty for now)
```

---

## 💻 CLI Usage

```bash
python json2apex.py input.json -o Student.cls -c Student
```

## 📄 Arguments

| Flag         | Description                       |
| ------------ | --------------------------------- |
| `input.json` | Path to your input JSON file      |
| `-o`         | Output Apex class file (.cls)     |
| `-c`         | Root class name (default: `Root`) |

## 📂 Example

🔸 Input JSON: input.json

```
{
  "class": "Math",
  "score": 95,
  "details": {
    "public": true,
    "remarks": "Excellent"
  }
}
```

🔸 Command

```bash
python json2apex.py input.json -o Student.cls -c Student
```

🔸 Output Apex Class: Student.cls

```
public class Student {
    public String _class; // "class" -> _class
    public Integer score;
    public Details details;

    public static Student fromJSON(String json) {
        return (Student) JSON.deserialize(json, Student.class);
    }

    public String toJSON() {
        return JSON.serialize(this);
    }

    public class Details {
        public Boolean _public; // "public" -> _public
        public String remarks;
    }
}
```
