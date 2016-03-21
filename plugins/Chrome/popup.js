function getCurrentTabUrl(callback) {
  var queryInfo = {
    active: true,
    currentWindow: true
  };

  chrome.tabs.query(queryInfo, function(tabs) {
    var tab = tabs[0];
    var url = tab.url;

    console.assert(typeof url == 'string');
    callback(url);
  });
}

function renderStatus(url) {
  document.getElementById('label').value = url;
}

function analyze_project(url) {
    url = "http://www.drscratch.org/plugin/" + url
    //window.open(url, "Dr. Scratch", "directories=no, location=no, menubar=no, scrollbars=yes, statusbar=no, tittlebar=no, width=400, height=400");
    window.open(url, '_blank');
}

document.addEventListener('DOMContentLoaded', function() {
  getCurrentTabUrl(function(url) {
      url = url.split("/#")[0];
      renderStatus(url);
  });

  var button = document.getElementById('button');
  button.addEventListener('click', function() {
    getCurrentTabUrl(function(url) { 
        analyze_project(url);
    });
  });
});
