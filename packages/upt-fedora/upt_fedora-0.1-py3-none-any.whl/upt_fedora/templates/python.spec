{% extends 'base.spec' %}
{% block globals %}
%global srcname {{ pkg.sourcename }}
{% endblock %}

{% block requirements %}
  {% for pythonversion in [2, 3] %}
    {% if not loop.first %}

    {% endif %}
%package -n python{{ pythonversion }}-%{sname}
Summary:	{{ pkg.summary }}
    {% for build_dep in pkg.build_depends %}
BuildRequires:	{{ build_dep | reqformat(pythonversion) }}
    {% endfor %}
# Tests
    {% for test_dep in pkg.test_depends %}
BuildRequires:	{{ test_dep | reqformat(pythonversion) }}
    {% endfor %}

    {% for run_dep in pkg.run_depends %}
Requires:	{{ run_dep | reqformat(pythonversion)}}
    {% endfor %}

%description -n python{{ pythonversion }}-%{sname}
TODO
  {% endfor %}
{% endblock requirements%}

{% block build %}
%build
%py2_build
%py3_build
{% endblock %}

{% block install %}
%install
%py2_install
%py3_install
{% endblock %}
