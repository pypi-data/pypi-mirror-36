FROM {{base_image}}

RUN rm -f /usr/local/bin/python
RUN ln -s /usr/local/bin/{{python}} /usr/local/bin/python

RUN ln -s /usr/local/bin/{{pip}} /usr/local/bin/pip

WORKDIR /orchestrate

ADD "." "/"

# Install the user's dependencies
{{#install_commands}}
RUN {{.}}
{{/install_commands}}
