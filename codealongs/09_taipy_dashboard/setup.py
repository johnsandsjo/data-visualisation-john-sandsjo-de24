from setuptools import setup, find_packages

print(find_packages())

setup(
    name= "yh-dashboard",
    version = "0.0.1",
    description = """
    This package is used for creating YH dashboard
    """,
    author = "John Sandsjö",
    author_emai = "john.sandsjo@sti.stud.se",
    install_requires = ["pandas", "taipy", "duckdb", "openpyxl"],
    packages = find_packages(exclude= ("test*", "explorations", "assets", "data"))
)