/*
 * cbeta.js
 *
 * Date: 2019-07-30
 */

//------------------全局变量及函数---------------

var mulu_info = '';

function view_sutra(page_code, clear_mulu) {
  postApi('/cbeta/sutra', {'data': {'page_code': page_code.trim()}}, function (res) {
    // 设置经文内容
    $('#content-article').html(res.content);
    // 设置全局变量
    zang = res.zang;
    jing = res.jing;
    juan = res.juan;
    prev = res.prev;
    next = res.next;
    // 设置经文卷导航
    var first = res.juan_list[0];
    var last = res.juan_list[res.juan_list.length - 1];
    $('.sub-line .article .btn-page.first').attr('title', first);
    $('.sub-line .article .btn-page.last').attr('title', last);
    $('.sub-line .article .btn-page.prev').attr('title', prev);
    $('.sub-line .article .btn-page.next').attr('title', next);
    $('.sub-line .article .btn-page.to input').val(juan);
    $('.sub-line .article .total').text(last);
    // 清空目录信息
    if (clear_mulu === undefined || clear_mulu)
      mulu_info = '';
    // 隐藏弹框
    hide_dlg();
    // 设置锚点
    window.location.hash = page_code;

  });
}

var last_query = '';

function search(q, page) {
  if (q === '' || parseInt(page) < 1) return;
  postApi('/cbeta/search', {'data': {'q': q, 'page': page}}, function (res) {
    var html = '';
    for (var i = 0, len = res.data.hits.length; i < len; i++) {
      var hit = res.data.hits[i];
      html += get_hit_html(hit['sutra_code'], hit['page_code'], hit['normal']);
    }
    $('.content-right .result-items').html(html);
    var totalPage = Math.ceil(res.data.total / 10);
    $('.sub-line .search .btn-page.last').attr('title', totalPage);
    $('.sub-line .search .btn-page.to input').val(page);
    $('.content-right').removeClass('hide');
    $('.sub-line .right').removeClass('hide');
    // 设置全局变量
    last_query = q;
  });
}

function _get_sutra_maps() {
  var sutra_maps = [];
  for (var i = 0, len = cbeta_sutras.length; i < len; i++) {
    sutra_maps[cbeta_sutras[i][0]] = cbeta_sutras[i];
  }
  return sutra_maps;
}

var sutra_maps = _get_sutra_maps();

function _get_sutra_tips(sutra_code) {
  var sutra = sutra_maps[sutra_code];
  if (sutra !== undefined)
    return sutra[1] + '(' + sutra[5] + '卷)[' + sutra[7] + ']';
}

function get_hit_html(sutra_code, page_code, text) {
  var head = '<div class="result-head"><span class="btn-nav prev-page"><</span><span class="title">' + page_code
      + '</span><span class="btn-nav next-page">></span><img class="btn-img btn-show-pic" src="/static/imgs/icon_pic.png">'
      + '<img class="btn-img btn-stick"></div>';
  var name = '<div class="result-name">' + _get_sutra_tips(sutra_code) + '</div>';
  var text = '<div class="result-text slim-scroll">' + text + '</div>';
  return '<div class="result-item">' + head + name + text + '</div>';
}

function hide_dlg() {
  $('#text-selected-dlg').hide();
  $('#note-click-dlg').hide();
}

function pad(num, len) {
  num += "";
  return num.length < len ? num.padStart(len, "0") : num;
}

//------------------页面初始化------------------

// 高度自适应
$(document).ready(function () {
  var h = $(document.body).height();
  $('#main-left').height(h);
  $('#main-right').height(h);
});

$(window).resize(function () {
  var h = $(document.body).height();
  $('#main-left').height(h);
  $('#main-right').height(h);
});

window.location.hash = '';

//------------------顶部导航--------------------

// 显示、隐藏文章区域
$('.m-header .zone-control .zone-article').click(function () {
  $('.main-right .content .content-left').toggleClass('hide');
  $('.m-header .sub-line .left').toggleClass('hide');
  hide_dlg();
});

// 显示、隐藏中间区域
$('.m-header .zone-control .zone-stick').click(function () {
  $('.main-right .content .content-center').toggleClass('hide');
  $('.m-header .sub-line .center').toggleClass('hide');
  hide_dlg();
});

// 显示、隐藏检索区域
$('.m-header .zone-control .zone-search').click(function () {
  $('.main-right .content .content-right').toggleClass('hide');
  $('.m-header .sub-line .right').toggleClass('hide');
  hide_dlg();
});

//------------------左侧经文--------------------

// 展开更多操作
$('.sub-line .more .btn-more').click(function () {
  $('.more-group').toggleClass('hidden');
});

$('.sub-line .more .btn-sm').click(function () {
  $(this).toggleClass('active');
});

// 显示经文行首
$('.sub-line .more .btn-line-head').click(function () {
  if ($('#content-article').hasClass('article-row'))
    $('#content-article').removeClass('article-row').addClass('article');
  else
    $('#content-article').removeClass('article').addClass('article-row');
});

// 显示经文校勘
$('.sub-line .more .btn-note').click(function () {
  if ($(this).hasClass('active')) {
    $('.content-left .note').hide();
  } else {
    $('.content-left .note').show();
    $('.content-left .note.mod').hide();
  }
});

// 显示经文标点
$('.sub-line .more .btn-bd').click(function () {
  if ($(this).hasClass('active'))
    $('.content-left bd').hide();
  else
    $('.content-left bd').show();
});

// 跳转第一卷
$('.sub-line .article .btn-page.first').click(function () {
  var n = $('.sub-line .left .btn-page.first').attr('title').toString();
  var page_code = zang + pad(jing, 4) + '_' + pad(n, 3);
  view_sutra(page_code, false);
});

// 跳转最末卷
$('.sub-line .article .btn-page.last').click(function () {
  var n = $('.sub-line .left .btn-page.last').attr('title').toString();
  var page_code = zang + pad(jing, 4) + '_' + pad(n, 3);
  view_sutra(page_code, false);
});

// 跳转上一卷
$('.sub-line .article .btn-page.prev').click(function () {
  var page_code = zang + pad(jing, 4) + '_' + pad(prev, 3);
  view_sutra(page_code, false);
});

// 跳转下一卷
$('.sub-line .article .btn-page.next').click(function () {
  var page_code = zang + pad(jing, 4) + '_' + pad(next, 3);
  console.log(page_code);
  view_sutra(page_code, false);
});

// 跳转第n卷
$('.sub-line .article .btn-page.to').on("keydown", function (event) {
  var keyCode = event.keyCode || event.which;
  if (keyCode == "13") {
    var n = $('.btn-page.to input').val().trim();
    var page_code = zang + pad(jing, 4) + '_' + pad(n, 3);
    view_sutra(page_code, false);
  }
});

// 增加经文字体
$('.sub-line .article .btn-font-enlarge').click(function () {
  var $article = $('.content > .content-left');
  var cur_size = parseFloat($article.css('font-size'));
  $article.css('font-size', cur_size + 1);
});

// 减少经文字体
$('.sub-line .article .btn-font-reduce').click(function () {
  var $article = $('.content > .content-left');
  var cur_size = parseFloat($article.css('font-size'));
  $article.css('font-size', cur_size - 1);
});

// 收起第二行导航
$('.zoom .min-img').click(function () {
  $('.zoom .min-img').toggleClass('hide');
  $('.zoom .max-img').toggleClass('hide');
  $('.m-header .sub-line').hide();
  $('.main-right .content').css('padding-top', 40);
});

// 展开第二行导航
$('.zoom .max-img').click(function () {
  $('.zoom .min-img').toggleClass('hide');
  $('.zoom .max-img').toggleClass('hide');
  $('.m-header .sub-line').show();
  $('.main-right .content').css('padding-top', 70);
});


// 点击经文校勘记，显示弹框
$('#content-article').on('click', '.note', function (e) {
  var $note_dlg = $('#note-click-dlg');
  var positionX = e.pageX;
  var positionY = e.pageY;
  var height = window.screen.availHeight;
  var width = $('.main-right .content-left').width();
  var left_distance = $('.main-right .content-left').offset().left;
  var screenY = e.screenY;
  var dlg_width = $note_dlg.width();
  var dlg_height = $note_dlg.height();
  if (positionX + dlg_width > width + left_distance) {
    $note_dlg.css('left', positionX - dlg_width - 30);
  } else {
    $note_dlg.css('left', positionX);
  }
  if (screenY + dlg_height > height) {
    $note_dlg.css('top', positionY - dlg_height - 30);
  } else {
    $note_dlg.css('top', positionY + 10);
  }
  $note_dlg.find('.title').text($(this).attr('data-title'));
  $note_dlg.find('.content').text($(this).attr('data-content'));
  $note_dlg.show();
  $('#text-selected-dlg').hide();
});

// 选中经文文字，显示弹框
$('.main-content .content-left').mouseup(function (e) {
  var $txt_dlg = $('#text-selected-dlg');
  var txt = window.getSelection ? window.getSelection() : document.selection.createRange().text; //选中的文本
  if (txt.toString().length > 0) {
    var positionX = e.pageX;
    var positionY = e.pageY;
    var screenY = e.screenY;
    var width = $('.main-right .content').width();
    var left_distance = $('.main-right .content').offset().left;
    var height = window.screen.availHeight;
    var dlg_width = $txt_dlg.width();
    var dlg_height = $txt_dlg.height();
    if (positionX + dlg_width > width + left_distance) {
      $txt_dlg.css('left', positionX - dlg_width - 30);
    } else {
      $txt_dlg.css('left', positionX);
    }
    if (screenY + dlg_height > height) {
      $txt_dlg.css('top', positionY - dlg_height - 30);
    } else {
      $txt_dlg.css('top', positionY + 10);
    }
    $txt_dlg.show();
    $('#note-click-dlg').hide();
  } else {
    //点击空白处，取消弹框
    $('#text-selected-dlg').hide();
    $('#note-click-dlg').hide();
  }
});

// 复制文字
$('#text-selected-dlg #copy-text').click(function () {
  document.execCommand("copy");
  $('#text-selected-dlg').hide();
});

// 引用复制
$('#text-selected-dlg #cite-copy').click(function () {
  document.execCommand("copy");
  $('#text-selected-dlg').hide();
});

// 全文检索
$('#text-selected-dlg #full-search').click(function () {
  var txt = window.getSelection ? window.getSelection() : document.selection.createRange().text;
  console.log(txt);
  $('.m-header #search-input').val(txt.toString());
  $('.m-header #btn-search').click();
  $('#text-selected-dlg').hide();
});

// 查看图片
$('#text-selected-dlg #view-pic').click(function () {
  document.execCommand("copy");
  $('#text-selected-dlg').hide();
});


//------------------右侧全文检索-----------------

// 全文检索
$('.m-header #btn-search').click(function () {
  var q = $('.m-header #search-input').val().trim();
  search(q, 1);
});

$('.m-header #search-input').on("keydown", function (event) {
  var keyCode = event.keyCode || event.which;
  if (keyCode == "13") {
    var q = $('.m-header #search-input').val().trim();
    search(q, 1);
  }
});

// 检索结果集-跳转第一页
$('.sub-line .search .btn-page.first').click(function () {
  search(last_query, 1);
});

// 检索结果集-跳转最末页
$('.sub-line .search .btn-page.last').click(function () {
  var page = $('.sub-line .search .btn-page.last').attr('title');
  search(last_query, page);
});

// 检索结果集-跳转上一页
$('.sub-line .search .btn-page.prev').click(function () {
  var page = $('.sub-line .search .btn-page.to input').val();
  search(last_query, parseInt(page) - 1);
});

// 检索结果集-跳转下一页
$('.sub-line .search .btn-page.next').click(function () {
  var page = $('.sub-line .search .btn-page.to input').val();
  search(last_query, parseInt(page) + 1);
});

// 检索结果集-跳转第n页
$('.sub-line .search .btn-page.to').on("keydown", function (event) {
  var keyCode = event.keyCode || event.which;
  if (keyCode == "13") {
    var page = $('.sub-line .search .btn-page.to input').val();
    search(last_query, page);
  }
});

// 检索结果集-增加字体
$('.sub-line .search .btn-font-enlarge').click(function () {
  var $resultItem = $('.content-right .result-item');
  var cur_size = parseFloat($resultItem.css('font-size'));
  $resultItem.css('font-size', cur_size + 1);
});

// 检索结果集-减少字体
$('.sub-line .search .btn-font-reduce').click(function () {
  var $resultItem = $('.content-right .result-item');
  var cur_size = parseFloat($resultItem.css('font-size'));
  $resultItem.css('font-size', cur_size - 1);
});

// 检索结果-点击页码-查看该页经文
$('.result-items').on('click', '.result-head .title', function () {
  view_sutra($(this).text().trim());
});

// 检索结果-上一页
$('.result-items').on('click', '.result-head .prev-page', function () {
  var item = $(this).parent().parent();
  var cur_page_code = item.find('.title').text();
  postApi('/cbeta/prev_page', {'data': {'cur_page_code': cur_page_code}}, function (hit) {
    var html = get_hit_html(hit['sutra_code'], hit['page_code'], hit['normal']);
    item.prop('outerHTML', html);
  });
});

// 当前结果-下一页
$('.result-items').on('click', '.result-head .next-page', function () {
  var item = $(this).parent().parent();
  var cur_page_code = item.find('.title').text();
  postApi('/cbeta/next_page', {'data': {'cur_page_code': cur_page_code}}, function (hit) {
    var html = get_hit_html(hit['sutra_code'], hit['page_code'], hit['normal']);
    item.prop('outerHTML', html);
  });
});

// 当前结果-查看图片
$('.result-items').on('click', '.result-head .btn-show-pic', function () {
  var item = $(this).parent().parent();
  var page_code = item.find('.title').text();
  postApi('/cbeta/img_url', {'data': {'page_code': page_code}}, function (res) {
    var img_url = res.img_url;
    console.log(img_url);
    $('#picModal #sutra-img').attr('src', img_url);
    $('#picModal').modal();
  });
});

// 当前结果-粘住
$('.content-right .result-items').on('click', '.result-head .btn-stick', function () {
  $('.main-right .content .content-center').removeClass('hide');
  $('.m-header .sub-line .center').removeClass('hide');
  $('.content-center .result-items').append($(this).parent().parent());
});


// 配置自定检索范围
$('#my-select').multiSelect({
  selectableHeader: "待选经名<input type='text' class='form-control search-input' id='selectable_input' placeholder='您可以输入关键字进行搜索'>",
  selectionHeader: "已选经名<input type='text' class='form-control search-input' id='selected_input' placeholder='您可以输入关键字进行搜索'>",
  selectableFooter: "<a class='left_btn' id='select_all_btn'>全选</a><a class='right_btn' id='select_all_search_btn'>全选所有搜索结果</a>",
  selectionFooter: "<a class='left_btn' id='deselect_all_btn'>全删</a><a class='right_btn' id='deselect_all_search_btn'>删除所有搜索结果</a>",
  selectableOptgroup: true,
  afterSelect: function (val) {
    console.log(val);
  }
});

// 选中、新增检索分组
function dblClickCheckbox() {
  $('#searchConfigModal .checkbox-inline').removeClass('active');
  $(this).addClass('active');
  $('.cur-search-scope').text($(this).text());
}

$('#searchConfigModal .checkbox-inline').bind('dblclick', dblClickCheckbox);

$('#searchConfigModal .add-search-scope').click(function () {
  var scopeStr = "<span class='search-scope'><input type='checkbox'/><label class='checkbox-inline' contenteditable='true'>新建</label></span>";
  $('#searchConfigModal .search-scope-groups').append(scopeStr);
  $('#searchConfigModal .search-scope-groups .checkbox-inline:last').focus();
  $('#searchConfigModal .checkbox-inline').unbind('dblclick').bind('dblclick', dblClickCheckbox);
});

// 选择检索范围
$('.scope-item').click(function () {
  $('.scope-item').removeClass('active');
  $(this).addClass('active');
  $('#cur-scope').text($(this).text());
});


//------------------中间粘住检索结果--------------

// 检索结果集-增加字体
$('.sub-line .stick .btn-font-enlarge').click(function () {
  var $resultItem = $('.content-center .result-item');
  var cur_size = parseFloat($resultItem.css('font-size'));
  $resultItem.css('font-size', cur_size + 1);
});

// 检索结果集-减少字体
$('.sub-line .stick .btn-font-reduce').click(function () {
  var $resultItem = $('.content-center .result-item');
  var cur_size = parseFloat($resultItem.css('font-size'));
  $resultItem.css('font-size', cur_size - 1);
});

// 删除粘住的结果
$('.content-center .result-items').on('click', '.result-head .btn-stick', function () {
  $(this).parent().parent().remove();
});

//------------------经目检索---------------------

// Datatable本地化
var language = {
  "sProcessing": "处理中...",
  "sLengthMenu": "显示 _MENU_ 项结果",
  "sZeroRecords": "没有匹配结果",
  "sInfo": "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
  "sInfoEmpty": "显示第 0 至 0 项结果，共 0 项",
  "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
  "sInfoPostFix": "",
  "sSearch": "搜索:",
  "sUrl": "",
  "sEmptyTable": "表中数据为空",
  "sLoadingRecords": "载入中...",
  "sInfoThousands": ",",
  "oPaginate": {
    "sFirst": "首页",
    "sPrevious": "上页",
    "sNext": "下页",
    "sLast": "末页"
  },
  "oAria": {
    "sSortAscending": ": 以升序排列此列",
    "sSortDescending": ": 以降序排列此列"
  }
};

// DataTable-初始化
$('#my-sutra-table').DataTable({
  language: language,
  data: cbeta_sutras,
  columnDefs: [
    {
      'targets': [0],
      'data': 'id',
      'render': function (data, type, full) {
        return '<span class="sutra-code">' + full[0] + '</span>'
      }
    }
  ]
});

$('#my-sutra-table').on("click", '.sutra-code', function (event) {
  view_sutra($(this).text(), true);
  $('#sutraNavModal').modal('hide');

});

//------------------目录导航---------------------

$('#my-mulu-tree').jstree({'core': {'data': null}});

$('#muluModal').on('shown.bs.modal', function (e) {
  if (mulu_info === '') {
    postApi('/cbeta/mulu', {'data': {'zang': zang, 'jing': jing}}, function (res) {
      mulu_info = res.data;
      $('#my-mulu-tree').jstree(true).settings.core.data=mulu_info;
      $('#my-mulu-tree').jstree(true).refresh();
    });
  }
});

// 双击目录节点时，打开链接
$('#my-mulu-tree').bind("dblclick.jstree", function (event) {
  var node = $(event.target).closest("li");
  view_sutra(node.attr('title'), false);
  $('#muluModal').modal('hide');
});