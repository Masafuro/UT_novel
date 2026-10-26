"""CLI entrypoint for UT_novel."""
import click
import os
from ut_novel.engine import NovelEngine

@click.group()
def main():
    """UT_novel: Undertale-style dialogue video generator."""
    pass

@main.command()
@click.option("--script", "-s", required=True, type=click.Path(exists=True), help="Path to markdown dialogue script.")
@click.option("--output", "-o", default="output/output.mp4", help="Path to output MP4 video file.")
@click.option("--aspect-ratio", "-a", type=click.Choice(["16:9", "9:16"], case_sensitive=False), default=None, help="Override aspect ratio (16:9 or 9:16 for Shorts).")
@click.option("--fps", type=int, default=None, help="Override frame rate (e.g., 30 or 60).")
@click.option("--preview-sec", type=float, default=None, help="Only render the first N seconds for quick testing.")
def render(script, output, aspect_ratio, fps, preview_sec):
    """Render a full dialogue video from a Markdown script."""
    os.makedirs(os.path.dirname(os.path.abspath(output)), exist_ok=True)
    engine = NovelEngine()
    engine.render_script_to_video(
        script_path=script,
        output_path=output,
        override_aspect_ratio=aspect_ratio,
        override_fps=fps,
        preview_seconds=preview_sec
    )

if __name__ == "__main__":
    main()
