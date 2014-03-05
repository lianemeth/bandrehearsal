<%inherit file="base.mako" />
<%block name="xtra_js">
% for jsfile in requirements['js']:
	<script type="text/javascript" src="${request.static_url(jsfile)}"></script>
% endfor
</%block>
<%block name="xtra_style">
% for cssfile in requirements['css']:
	<link rel="stylesheet" type="text/css" href="${request.static_url(cssfile)}" />
% endfor
</%block>
<%block name="after_content">
<script type="text/javascript">
deform.load();
</script>
</%block>
