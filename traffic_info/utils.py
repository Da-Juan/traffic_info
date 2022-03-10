"""Utils for traffic_info package."""
import shutil
from typing import Any, Dict

import jinja2

Context = Dict[str, Any]


def get_chromedriver_path() -> str:
    """
    Get ChromeDriver's binary path.

    Returns:
        The ChromeDriver's binary path, None otherwise.

    """
    chromedriver_path = shutil.which("chromedriver")
    return chromedriver_path


def render_template(template: str, context: Context, output: str = None) -> str:
    """
    Render a Jinja2 template.

    Args:
        template: The path to the Jinja2 template.
        context: The Jinja2 context.
        output: The path to save the rendered file.

    Returns:
        The rendered template if output is None or the path to the rendered file.

    """
    with open(template, mode="r", encoding="utf-8") as template_file:
        jinja_template = jinja2.Template(template_file.read())

    render = jinja_template.render(context)
    if output is None:
        return render
    with open(output, mode="w", encoding="utf-8") as render_file:
        render_file.write(render)
    return output
