# PyTest Ethereum Plugin
*py.test plugin for testing Ethereum Smart Contracts*

---

# Usage

Step 1: Install
```bash
pip install pytest-ethereum  # python 3.6+
```

Step 2: Compile your contracts into a package (soon to be ethPM-compliant)
```bash
solc --combined-json abi,bin,bin-runtime contracts/ > contracts.json
```

Step 3. Execute your test suite (make sure to import your package file!)
```bash
py.test --package-file contracts.json tests/
```

---

# Guidelines

1. This plugin is *opinionated*
    * There should only be *one way* to do something
    * Support for special needs is possible, but undesireable
2. This plugin is *intuitive*
    * It should be VERY clear how to use it
    * It should not get in the way of smart contract testing
    * It should remove the complexities of a production environment
3. This plugin is *concise*
    * Fixture API is simple and expressive
    * Write high quality tests quickly and easily

---

# Contributing

Rules:
1. Test cases should be grep'd from documentation
    * Unless they are uninteresting corner cases
2. Test cases should be well explained
3. Follow the Guidelines!
