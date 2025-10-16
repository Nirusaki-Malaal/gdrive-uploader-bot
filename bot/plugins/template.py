html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <title>FIERCENETWORK</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css">
  <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.slim.min.js"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
  <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.bundle.min.js"></script>
  <link rel = "icon" href="https://i.imgur.com/QGKe9iP.jpg" type = "image/x-icon">
</head>
<body>
<link rel="stylesheet" href="/css/anime_pages.css">
<link href="https://fonts.googleapis.com/css2?family=Comic+Neue&family=Poppins&family=Source+Sans+Pro&display=swap" rel="stylesheet"> 
<nav class="navbar navbar-expand-md bg-dark navbar-dark">
  <a class="navbar-brand" href="http://fierce-network.github.io">
    <img src="https://i.imgur.com/QGKe9iP.jpg" alt="Logo" style="width:40px;">
    Fierce Network</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#collapsibleNavbar">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="collapsibleNavbar">
    <ul class="navbar-nav">
      <li class="nav-item">
        <a class="nav-link" href="https://mradulkumar-glitch.github.io/page/about.html">About</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://t.me/AnimeTalksIndia" target="_blank">Contact</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://www.fiecenetwork2.blogspot.com" target="_blank">Blogs</a>
      </li>    
    </ul>
    <form class="form-inline" action="/search.py">
      <input class="form-control mr-sm-2" type="text" placeholder="Search">
      <button class="btn btn-success" type="submit">Search</button>
    </form>
  </div> 
</nav>
<br>
<div id="con3">
  <img id="anime" src="{image}" alt="Anime Photo"><div id="titles">{title}</div>
  <div id="info">
    <strong>{title}</strong><br>
    Synopsis : 
    <div class="synopsis">
      {synopsis}
</div>
  {link}
</div>
<div style="margin-bottom: 75px;">
  </div>
  <div>
    <a href="https://t.me/fierce_requests" class="fa fa-telegram"><span  style="font-family: Poppins;font-size : medium; color : white; padding : 10px"> Telegram</span></a><br>
  </div>
  <script>
    var coll = document.getElementsByClassName("collapsible");
    var i;

'''

remains = '''    
    for (i = 0; i < coll.length; i++) { 
      coll[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.maxHeight){
          content.style.maxHeight = null;
        } else {
          content.style.maxHeight = content.scrollHeight + "px";
        } 
      });
    }
    </script>  
</body>
</html>'''