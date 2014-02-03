<!DOCTYPE html>
<html>
	<head>
		<meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <link href="${request.static_url('bandrehearsal:static/css/screen.css')}" 
                        media="screen, projection" rel="stylesheet" type="text/css" />
                <link href="${request.static_url('bandrehearsal:static/css/foundation.css')}" 
                        media="screen, projection" rel="stylesheet" type="text/css" />
                <link href="${request.static_url('bandrehearsal:static/css/normalize.css')}" 
                        media="screen, projection" rel="stylesheet" type="text/css" />
                <link href="${request.static_url('bandrehearsal:static/css/print.css')}" 
                        media="print" rel="stylesheet" type="text/css" />
                <!--[if IE]>
                      <link href="S{request.static_url('bandrehearsal:static/css/ie.css')}" 
                        media="screen, projection" rel="stylesheet" type="text/css" />
               <![endif]-->

               <%block name="xtra_style" />
	       <script type="text/javascript" src="${request.static_url('bandrehearsal:static/js/jquery.js')}"></script>
	       <script type="text/javascript" src="${request.static_url('bandrehearsal:static/js/modernizr.js')}"></script>
	       <script type="text/javascript" src="${request.static_url('bandrehearsal:static/js/foundation.min.js')}"></script>
	       <script type="text/javascript" src="${request.static_url('bandrehearsal:static/js/app.js')}"></script>
               <%block name="xtra_js" />
	</head>
	<body>
		<%block name="content" />
	</body>
</html>
