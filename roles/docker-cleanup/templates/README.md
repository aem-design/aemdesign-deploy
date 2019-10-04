templates go here, templates end in .j2,
========

Source

* [template - Templates a file out to a remote server.](http://docs.ansible.com/ansible/template_module.html)

Templates are processed by the Jinja2 templating language (http://jinja.pocoo.org/docs/) - documentation on the template formatting can be found in the Template Designer Documentation (http://jinja.pocoo.org/docs/templates/). Six additional variables can be used in templates: ansible_managed (configurable via the defaults section of ansible.cfg) contains a string which can be used to describe the template name, host, modification time of the template file and the owner uid, template_host contains the node name of the template’s machine, template_uid the owner, template_path the absolute path of the template, template_fullpath is the absolute path of the template, and template_run_date is the date that the template was rendered. Note that including a string that uses a date in the template will result in the template being marked ‘changed’ each time.