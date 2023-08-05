FROM {{base_image}}

ADD "." "/"

# Install the user's dependencies
{{#install_commands}}
RUN {{.}}
{{/install_commands}}
