config_hierarchy = {
    "config.yaml": """
        defaults:
        - db: mysql
    """,
    "db": {
        "mysql.yaml": """
            defaults:
            - conn: https
            driver: mysql
            user: omry
            password: secret
            """,
        "postgresql.yaml": """
            driver: postgresql
            user: postgres_user
            password: drowssap
            timeout: 10
            """,
        "conn": {
            "http.yaml": """
                method: http
                port: 80
            """,
            "https.yaml": """
                method: https
                port: 443
            """,
        },
    },
}

experiments = [
    {
        "name": "default config",
        "config_hierarchy": config_hierarchy,
    },
    {
        "name": "basic group override",
        "config_hierarchy": config_hierarchy,
        "command_line_args": "db=postgresql",
    },
    {
        "name": "nested group override",
        "config_hierarchy": config_hierarchy,
        "command_line_args": "db/conn=http",
    },
]

if __name__ == "__main__":
    import os
    from ..config_examples import ExHydraConfig

    cur_dir = os.path.dirname(__file__)
    doc_dir = os.path.abspath(os.path.join(cur_dir, "..", "docs"))

    os.makedirs(doc_dir, exist_ok=True)
    file_basename = os.path.splitext(os.path.split(__file__)[-1])[0]
    out_name = os.path.join(doc_dir, f"{file_basename}.md")

    md = ""
    for ex in experiments:
        ex = ExHydraConfig(**ex)
        md += ex.to_markdown()

    print(md)

    with open(out_name, "w") as f:
        f.write(md)
