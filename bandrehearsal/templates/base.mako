<!DOCTYPE html>
<html>
	<head>
                <link href="${request.static_url('stylesheets/screen.css')}" 
                        media="screen, projection" rel="stylesheet" type="text/css" />
                <link href="${request.static_url('stylesheets/print.css')}" 
                        media="print" rel="stylesheet" type="text/css" />
                <!--[if IE]>
                      <link href="S{request.static_url('stylesheets/ie.css')}" 
                        media="screen, projection" rel="stylesheet" type="text/css" />
               <![endif]-->
               <%block name="xtra_style" />
               <%block name="xtra_js" />
	</head>
	<body>
	</body>
</html>
