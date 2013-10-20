#!/bin/bash
<%!
    import os
%><%
    LOG_DIR = os.path.join(INSTANCE_PATH, 'log', service_name)
%>

# Runit.
if [[ "$(which svlogd)" ]]; then
    exec svlogd "${LOG_DIR}"
fi

# Daemontools.
exec multilog n1000 "${LOG_DIR}"
