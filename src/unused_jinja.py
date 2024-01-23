# EXPLORE REPLACING ALGORITHMIC ADIF GENERATINO WITH JINJA TEMPLATE PROCESSING
import jinja2

def custom_func(a, b):
    return a + b

(tmpl_dir, tmpl_file) = os.path.split(self.input_path)

env = jinja2.Environment(loader=jinja2.FileSystemLoader(tmpl_dir),
                         trim_blocks=True, lstrip_blocks=True)

env.globals['custom_func'] = custom_func

self.template = env.get_template(tmpl_file)

self.content = self.template.render(dict(foo="001", bar="002"))
