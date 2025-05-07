# 🎄 pysleigh

**pysleigh** is a Python CLI tool to automate your [Advent of Code](https://adventofcode.com/) experience — fetch inputs, generate templates, run solutions, benchmark code, and even submit answers. All from the terminal.

---

## 📦 Installation

### Via pip (recommended)
```bash
pip install pysleigh
```

### Editable install for development
```bash
git clone https://github.com/your-username/pysleigh.git
cd pysleigh
pip install -e .[dev]
```

This gives you access to the `pysleigh` command globally.

---

## ⚙️ Configuration

Create a config file at `~/.config/pysleigh/config.toml`. Here’s a minimal example:

```toml
session_cookie = "566a.....319"

[inputs]
path = "~/Workspace/advent-of-code/input/"
format = "year_{year}/input_{year}_dayday:02d}.txt"

[articles]
path = "~/Workspace/advent-of-code/articles/"
format = "year_{year}/article_{year}_day_{day:02d}.md"

[solutions]
path = "~/Workspace/advent-of-code/solutions/python/"
format = "year_{year}/solution_{year}_day_{day:02d}.py"

[tests]
path = "~/Workspace/advent-of-code/tests/python/"
format = "year_{year}/test_{year}_day_{day:02d}.py"

[answers]
path = "~/Workspace/advent-of-code/answers/"
format = "year_{year}/answer_{year}_day{day:02d}.txt"

[template] # Optional
solution_path = "~/.config/pysleigh/solution_template.py"
test_path = "~/.config/pysleigh/test_template.py"
```

To get your session cookie:

1. Log into [Advent of Code](https://adventofcode.com/) in your browser.
2. Copy your session cookie from dev tools.
3. Paste it as `session_cookie = "..."` above.

---

## 🚀 CLI Usage

### General command structure

```bash
pysleigh <command> <subcommand> [options]
```

### Examples

#### 🧲 Fetch data
`bash
pysleigh fetch input --year 2022 --day 1
pysleigh fetch article --year 2022 --day 1
pysleigh fetch answer --year 2022 --day 1
```

#### ⚙️ Generate code
```bash
pysleigh generate solution --year 2022 --day 1
pysleigh generate test --year 2022 --day 1
```

#### 🧪 Run solutions & tests
```bash
pysleigh run solution --year 2022 --day 1
pysleigh run test --year 202 --day 1
```

#### 🧰 Prep an entire day
```bash
pysleigh prep solution --year 2022 --day 1
pysleigh prep test --year 2022 --day 1
```

#### ⏱️ Benchmark performance
```bash
pysleigh benchmark solution --year 2022 --day 1 --runs 10
```

#### ✅ Submit your answer
```bash
pysleigh submit answer --year 2022 --day 1 --part 1 --answer 42
```

If you omit `--answer`, it will compute the answer from your solution.

---

## 📄 License

MIT License © 2025 David Bateman
