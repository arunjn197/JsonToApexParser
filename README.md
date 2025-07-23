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
