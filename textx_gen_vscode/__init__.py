import os
import logging
import sys
import tempfile
import zipfile
from pathlib import Path

import click
from textx import generator, language_descriptions
from textx.registration import GeneratorParam
from textx_gen_coloring.generators import generate_textmate_syntax
from textxjinja import textx_jinja_generator


logger = logging.getLogger(__name__)


@generator("textX", "vscode", [
    GeneratorParam("project_name", "The name of the project used in vsix"),
    GeneratorParam("published", "The published of the vsix", False),
    GeneratorParam("version", "Version of the vsix", False),
    GeneratorParam("repository", "Git repository of the extension", False),
    GeneratorParam("description", "The description of the extension", False),
    GeneratorParam("skip_keywords", "Should keyword processing be done", False),
])
def vscode_gen(
    _metamodel,
    _model,
    output_path,
    overwrite,
    _debug,
    project_name,
    publisher="textX",
    version="0.1.0",
    repository="https://github.com/textX/textX-LS",
    description="textX DSL",
    skip_keywords=False
):
    """Generating VS Code extension for installed textX projects."""
    template_folder = Path(os.path.dirname(__file__)) / 'template'

    with tempfile.TemporaryDirectory() as tmpdirname:
        languages = _get_languages_by_project_name(project_name)
        if not languages:
            click.echo(f'\nError: No languages found for project "{project_name}".'
                        '\nCheck if the project exists in the current environment.')
            sys.exit(1)

        context = {
            'project_name': project_name,
            'publisher': publisher,
            'version': version,
            'repository': repository,
            'description': description,
            'languages': languages,
        }

        textx_jinja_generator(template_folder, tmpdirname,
                              context=context,
                              overwrite=overwrite)

        # Generate syntax highlighting
        syntaxes_path = Path(tmpdirname) / "extension" / "syntaxes"
        os.makedirs(syntaxes_path, exist_ok=True)
        for lang in languages:
            lang_name = lang.name.lower()
            lang_syntax_path = syntaxes_path / f"{lang_name}.json"
            lang_syntax_path.write_text(
                generate_textmate_syntax(
                    lang.metamodel, lang_name, skip_keywords=skip_keywords
                )
            )

        if output_path is None:
            output_path = f"{project_name}-{version}.vsix"

        create_vsix(output_path, tmpdirname)


def _is_same_project(project_name1, project_name2):
    """Compare projects.
    In some cases dash is converted to underscore, but the project is the same.
    """

    def _replace(name):
        return name.replace("-", "_").lower()

    return _replace(project_name1) == _replace(project_name2)


def _get_languages_by_project_name(project_name):
    """Get registered languages by project name."""
    return [
        lang
        for lang in language_descriptions().values()
        if _is_same_project(lang.project_name, project_name)
    ]


def create_vsix(vsix_file, tmp_folder):
    tmp_folder = Path(tmp_folder)
    with zipfile.ZipFile(vsix_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(tmp_folder):
            for file in files:
                file_path = Path(root) / file
                # Store relative path inside the zip
                arcname = file_path.relative_to(tmp_folder)
                zipf.write(file_path, arcname)

    logger.info("Created %s", vsix_file)
