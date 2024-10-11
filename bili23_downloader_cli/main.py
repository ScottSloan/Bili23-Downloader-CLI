import typer

app = typer.Typer()


@app.command()
def hello(name: str):
    print(f"hello {name}")


@app.command()
def goodbye(name: str):
    print(f"bye~ {name}")


def main():
    app()


@app.command(name="info", help="获取视频信息")
def get_url_info(url: str):
    print(f"this is url {url} info:xxxxx")


if __name__ == "__main__":
    app()
