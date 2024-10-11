from typing import Annotated, List, Optional
from typer import Exit, Typer, Argument, Option

from bili23_downloader_cli.cli.common import check_ffmpeg_available

app = Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Bilibili视频下载器",
    epilog="Made with :heart:  in [blue]Seven Dreamer[/blue]"
)

@app.command("version")
def show_version():
    """Show version"""
    version = "2.0.1"
    print(f"bili23 Downloader CLI Version: {version}")



# @app.command("info", help="Get video info")
# def get_url_info(url: str):
#     """获取视频信息"""
#     print(f"this is url {url} info:xxxxx")

@app.command(help="Download video",no_args_is_help=True)
def download(
    url: Annotated[List[str], Argument(help="视频链接",show_default=False)]
):
    """下载视频"""
    print(f"downloading ... {url}")

@app.command()
def config():
    """
    cli 配置
    """

@app.callback()
def main(
    # version: Annotated[bool, Option(callback=show_version, is_eager=True)] = False,
):
    """下载bilibili的视频"""
    check_ffmpeg_available()


if __name__ == "__main__":
    app()
