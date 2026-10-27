"""CLI entrypoint for UT_novel."""
import click
import os
from ut_novel.engine import NovelEngine
from ut_novel.templates import TemplateRegistry

@click.group()
def main():
    """UT_novel: Multi-template dialogue video generator."""
    pass

@main.command()
def templates():
    """List all available dialogue templates."""
    all_tmpl = TemplateRegistry.list_templates()
    click.echo("Available Dialogue Templates:")
    for t_name in sorted(all_tmpl):
        t = TemplateRegistry.get(t_name)
        click.echo(f"  - {t_name:18} ({t.screen_width}x{t.screen_height})")

@main.command()
@click.option("--script", "-s", required=True, type=click.Path(exists=True), help="Path to markdown dialogue script.")
@click.option("--output", "-o", default="output/output.mp4", help="Path to output MP4 video file.")
@click.option("--template", "-t", type=str, default=None, help="Override template (e.g. undertale_16_9, undertale_9_16, r4_16_9, r4_9_16).")
@click.option("--aspect-ratio", "-a", type=click.Choice(["16:9", "9:16"], case_sensitive=False), default=None, help="Legacy: Override aspect ratio.")
@click.option("--fps", type=int, default=None, help="Override frame rate (e.g., 30 or 60).")
@click.option("--preview-sec", type=float, default=None, help="Only render the first N seconds for quick testing.")
def render(script, output, template, aspect_ratio, fps, preview_sec):
    """Render a full dialogue video from a Markdown script."""
    os.makedirs(os.path.dirname(os.path.abspath(output)), exist_ok=True)
    engine = NovelEngine()
    engine.render_script_to_video(
        script_path=script,
        output_path=output,
        override_template=template,
        override_aspect_ratio=aspect_ratio,
        override_fps=fps,
        preview_seconds=preview_sec
    )

if __name__ == "__main__":
    main()
