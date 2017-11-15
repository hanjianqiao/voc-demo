function getParameterByName(name, url) {
  if (!url) url = window.location.href;
  name = name.replace(/[\[\]]/g, "\\$&");
  var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
     results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, " "));
}
function goCate(){
  window.location.href = 'category.html?cate_id=' + this.innerHTML;
}
(function startLoad(){
  var cate_id = getParameterByName('cate_id');
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var obj = JSON.parse(this.responseText);

      if(cate_id && cate_id != -1){
        var host = document.getElementById('top_category');
        var item = document.createElement('p');
        item.innerHTML = obj.Category.ParentId;
        item.onclick = goCate;
        host.appendChild(item);
      }

      var subHost = document.getElementById('category_list');
      for(var i = 0; i < obj.SubCategories.Category.length; i++){
        var item = document.createElement('p');
        item.innerHTML = obj.SubCategories.Category[i].CateId;
        item.onclick = goCate;
        subHost.appendChild(item);
      }

    }
  };
  xhttp.open("GET", "cate?cate_id="+cate_id, true);
  xhttp.send();
})();

function goVideo(){
  window.location.href = 'h5_player.html?video_id=' + this.video_id;
}

(function startLoad(){
  var cate_id = getParameterByName('cate_id');
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var obj = JSON.parse(this.responseText);

      if(cate_id && cate_id != -1){
        var host = document.getElementById('video_list');
        for(var i = 0; i < obj.VideoList.Video.length; i++){
          var item = document.createElement('img');
          item.src = obj.VideoList.Video[i].CoverURL;
          item.onclick = goVideo;
          item.video_id = obj.VideoList.Video[i].VideoId;
          host.appendChild(item);
        }
      }

    }
  };
  xhttp.open("GET", "list?id="+cate_id, true);
  xhttp.send();
})();
