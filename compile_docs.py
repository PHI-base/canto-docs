import functools
import glob
import markdown
import os
import re
from inspect import cleandoc

import lxml.html, lxml.etree

def newer_than(path1, path2):
    return os.stat(path1).st_mtime > os.stat(path2).st_mtime

def get_filename(path, ext=True):
    basename = os.path.basename(path)
    return basename if ext else os.path.splitext(basename)[0]

def generate_heading_ids(html):
    heading_tags = {'h1', 'h2', 'h3'}
    fragments = lxml.html.fragments_fromstring(html)
    for element in fragments:
        if element.tag in heading_tags:
            text = ''.join(element.itertext())
            id_text = re.sub(r'\W', '_', text.lower())
            element.set('id', id_text)
    return ''.join(
        lxml.etree.tostring(element, encoding=str, method='html')
        for element in fragments
    )

def link_html_images(html):
    image_link_elem = (
        '<a href="<% $c->uri_for($image_path . "/{image}") %>"/>'
        '<img class="screenshot"'
        ' src="<% $c->uri_for($image_path . "/{image}") %>'
        ' alt=""/>'
    )
    image_tmpl = cleandoc("""
    <div class="row-fluid">
    <div class="span6">
    {image_link}
    </div>
    </div>
    """.format(image_link=image_link_elem))
    image_re = re.compile(
        r'<p><img alt="" src="images/(?P<image>\w+\.png)" title=""\s*/?></p>'
    )
    out_lines = []
    for line in html.split('\n'):
        match = image_re.match(line)
        if match:
            image_name = match.group('image')
            out_lines.append(image_tmpl.format(image=image_name))
        else:
            out_lines.append(line)
    return '\n'.join(out_lines)

def add_catalyst_markup(html):
    template = cleandoc("""
    <!-- PAGE_TITLE: @@name@@ Documentation -->
    <!-- FLAGS: use_bootstrap -->
    {body}
    <%init>
    my $config = $c->config();
    my $base_docs_path = $config->{{base_docs_path}};
    my $image_path = '/static/images/' . $base_docs_path;
    </%init>
    """)
    return template.format(body=html)

def make_mhtml_from_md(in_dir, out_dir):
    markdown_paths = glob.glob(os.path.join(in_dir, '*.md'))

    for markdown_path in markdown_paths:
        with open(markdown_path, encoding='utf8') as markdown_file:
            markdown_doc = markdown_file.read()

        pipeline = (
            markdown.markdown,
            generate_heading_ids,
            link_html_images,
            add_catalyst_markup
        )
        mhtml_doc = functools.reduce(
            lambda x, f: f(x),
            pipeline,
            markdown_doc
        )

        markdown_filename = get_filename(markdown_path, ext=False)
        mhtml_filename = markdown_filename + '.mhtml'
        out_path = os.path.join(out_dir, mhtml_filename)

        write_args = {
            'mode': 'w+',
            'encoding': 'utf8',
            'newline': '\n'
        }
        with open(out_path, **write_args) as mhtml_file:
            mhtml_file.write(mhtml_doc + '\n')

def main():

    file_dir = os.path.abspath(os.path.dirname(__file__))
    docs_input_dir = os.path.join(file_dir, 'docs')

    output_dir = os.path.join(file_dir, 'build')

    make_mhtml_from_md(docs_input_dir, output_dir)

if __name__ == '__main__':
    main()
