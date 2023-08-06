String.prototype.format = function () {
  var args = arguments;
  return this.replace(/{(\d+)}/g, function (match, number) {
    return typeof args[number] != 'undefined' ? args[number] : match;
  });
};

function getCookie(name) {
  var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
  return r ? r[1] : undefined;
}

function setCookie(name, value, expires) {
  var domain = location.host.split(":")[0];
  if (expires) {
    var exp = new Date();
    exp.setTime(exp.getTime() + expires);
    document.cookie = name + "=" + value + ";path=/;domain=" + domain + ";expires=" + exp.toGMTString();
  } else {
    document.cookie = name + "=" + value + ";path=/;domain=" + domain + ";"
  }
}

function removeCookie(name) {
  setCookie(name, "", -1);
}

function parseUrl(url) {
  if (typeof url == 'undefined') {
    url = location.href;
  }
  var segment = url.match(/^(\w+\:\/\/)?([\w\d]+(?:\.[\w]+)*)?(?:\:(\d+))?(\/[^?#]*)?(?:\?([^#]*))?(?:#(.*))?$/);
  if (!segment[3]) {
    segment[3] = '80';
  }
  var param = {};
  if (segment[5]) {
    var pse = segment[5].match(/([^=&]+)=([^&]+)/g);
    if (pse) {
      for (var i = 0; i < pse.length; i++) {
        param[pse[i].split('=')[0]] = pse[i].split('=')[1];
      }
    }
  }
  return {
    url: segment[0],
    sechme: segment[1],
    host: segment[2],
    port: segment[3],
    path: segment[4],
    queryString: segment[5],
    fregment: segment[6],
    param: param
  };
};


$(function () {
  var clipboard = new ClipboardJS('.btn-copy', {
    target: function (trigger) {
      return $(trigger).parents('tr').find('input')[0]
    }
  })
  clipboard.on('success', function (e) {
    layer.msg('已复制到剪贴板', { time: 2000 })
    e.clearSelection()
  })

  clipboard.on('error', function (e) {
    layer.msg('复制出错，请手动复制', { time: 2000 })
  })
})
