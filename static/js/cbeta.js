/*
 * cbeta.js
 *
 * Date: 2019-07-30
 */

<!-- 页面初始化 -->

// 高度自适应
function adaptive() {
  var h = $(document.body).height();
  $('#main-left').height(h);
  $('#main-right').height(h);
}

$(document).ready(function () {
  adaptive();
});

$(window).resize(function () {
  adaptive();
});


<!-- 顶部导航 -->

// 显示、隐藏文章区域
$('.m-header .zone-control .zone-article').click(function () {
  $('.main-right .content .content-left').toggleClass('hide');
  $('.m-header .sub-line .left').toggleClass('hide');
});

// 显示、隐藏中间区域
$('.m-header .zone-control .zone-stick').click(function () {
  $('.main-right .content .content-center').toggleClass('hide');
  $('.m-header .sub-line .center').toggleClass('hide');
});

// 显示、隐藏检索区域
$('.m-header .zone-control .zone-search').click(function () {
  $('.main-right .content .content-right').toggleClass('hide');
  $('.m-header .sub-line .right').toggleClass('hide');
});


<!-- 左侧经文 -->

// 展开更多操作
$('.m-header .more .btn-more').click(function () {
  $('.more-group').toggleClass('hidden');
});

$('.m-header .more .btn-sm').click(function () {
  $(this).toggleClass('active');
});

// 显示经文行首
$('.m-header .more .btn-line-head').click(function () {
  if ($('#content-article').hasClass('article-row'))
    $('#content-article').removeClass('article-row').addClass('article');
  else
    $('#content-article').removeClass('article').addClass('article-row');
});

// 显示经文校勘
$('.m-header .more .btn-note').click(function () {
  if ($(this).hasClass('active')) {
    $('.content-left .note').hide();
  } else {
    $('.content-left .note').show();
    $('.content-left .note.mod').hide();
  }
});

// 显示经文标点
$('.m-header .more .btn-bd').click(function () {
  if ($(this).hasClass('active'))
    $('.content-left bd').hide();
  else
    $('.content-left bd').show();
});

// 跳转第一卷
$('.sub-line .article .btn-page.first').click(function () {
  var n = $('.sub-line .left .btn-page.first').css('title').toString();
  var juan = n.length < 3 ? n.padStart(3, "0") : n;
  window.location = '/' + zang + jing + '_' + juan;
});

// 跳转最末卷
$('.sub-line .article .btn-page.last').click(function () {
  var n = $('.sub-line .left .btn-page.last').css('title').toString();
  var juan = n.length < 3 ? n.padStart(3, "0") : n;
  window.location = '/' + zang + jing + '_' + juan;
});

// 跳转上一卷
$('.sub-line .article .btn-page.prev').click(function () {
  window.location = '/' + zang + jing + '_' + prev;
});

// 跳转下一卷
$('.sub-line .article .btn-page.next').click(function () {
  window.location = '/' + zang + jing + '_' + next;
});

// 跳转第n卷
$('.sub-line .article .btn-page.to').on("keydown", function (event) {
  var keyCode = event.keyCode || event.which;
  if (keyCode == "13") {
    var n = $('.btn-page.to input').val().trim();
    var juan = n.length < 3 ? n.padStart(3, "0") : n;
    window.location = '/' + zang + jing + '_' + juan;
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

// 展开、收起次导航
$('.zoom .min-img').click(function () {
  $('.zoom .min-img').toggleClass('hide');
  $('.zoom .max-img').toggleClass('hide');
  $('.m-header .sub-line').hide();
  $('.main-right .content').css('padding-top', 40);
});

$('.zoom .max-img').click(function () {
  $('.zoom .min-img').toggleClass('hide');
  $('.zoom .max-img').toggleClass('hide');
  $('.m-header .sub-line').show();
  $('.main-right .content').css('padding-top', 70);
});

// 点击经文关键字，显示弹框
$('#content-article .kw').click(function (e) {
  var $kw_dlg = $('#mouse-over-dlg');
  var positionX = e.pageX;
  var positionY = e.pageY;
  var height = window.screen.availHeight;
  var width = $('.main-right .content-left').width();
  var left_distance = $('.main-right .content-left').offset().left;
  var screenY = e.screenY;
  var dlg_width = $kw_dlg.width();
  var dlg_height = $kw_dlg.height();
  if (positionX + dlg_width > width + left_distance) {
    $kw_dlg.css('left', positionX - dlg_width - 30);
  } else {
    $kw_dlg.css('left', positionX);
  }
  if (screenY + dlg_height > height) {
    $kw_dlg.css('top', positionY - dlg_height - 30);
  } else {
    $kw_dlg.css('top', positionY + 10);
  }
  $kw_dlg.show();
  $('#text-selected-dlg').hide();
});

// 选中经文文字，显示弹框
$('.main-right .content p').mouseup(function (e) {
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
    $('#mouse-over-dlg').hide();
  } else {
    //点击空白处，取消弹框
    $('#text-selected-dlg').hide();
    $('#mouse-over-dlg').hide();
  }
});


<!-- 右侧全文检索 -->

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
    var totalPage = Math.ceil(res.data.total/10);
    $('.sub-line .search .btn-page.last').attr('title', totalPage);
    $('.sub-line .search .btn-page.to input').val(page);
    $('.content-right').removeClass('hide');
    $('.sub-line .right').removeClass('hide');
    // 设置全局变量
    last_query = q;
  });
}

function get_sutra_maps() {
  var sutra_maps = [];
  for (var i = 0, len = cbeta_sutras.length; i < len; i++) {
    sutra_maps[cbeta_sutras[i][0]] = cbeta_sutras[i];
  }
  return sutra_maps;
}
// 全局变量
var sutra_maps = get_sutra_maps();

function get_sutra_tips(sutra_code) {
  var sutra = sutra_maps[sutra_code];
  if (sutra != undefined)
    return sutra[1] + '(' + sutra[5] + '卷)[' + sutra[7] + ']';
}

function get_hit_html(sutra_code, page_code, text) {
  var head = '<div class="result-head"><span class="btn-nav prev-page"><</span><span class="title">' + page_code
      + '</span><span class="btn-nav next-page">></span><img class="btn-img btn-show-pic" src="/static/imgs/icon_pic.png">'
      + '<img class="btn-img btn-stick"></div>';
  var name = '<div class="result-name">' + get_sutra_tips(sutra_code) + '</div>';
  var text = '<div class="result-text slim-scroll">' + text + '</div>';
  return '<div class="result-item">' + head + name + text + '</div>';
}

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
  search(last_query, parseInt(page)-1);
});

// 检索结果集-跳转下一页
$('.sub-line .search .btn-page.next').click(function () {
  var page = $('.sub-line .search .btn-page.to input').val();
  search(last_query, parseInt(page)+1);
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

// 当前结果-点击page_code
$('.result-items').on('click', '.result-head .title', function () {
  var cur_page_code = $(this).text().trim();
  window.location = '/' + cur_page_code;
});


// 当前结果-上一页
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

// 弹框-检索结果排序方式
$('.sub-line .order-wrap').on('click', function (event) {
  event.stopPropagation();
  $('.search-orders').toggleClass('hide');
  var flag = true;
  var $tag = $('.search-orders');
  $tag.show();
  $(document).bind("click", function (e) {
    var target = $(e.target);
    if (target.closest($tag).length === 0 && flag === true) {
      $tag.hide();
      flag = false;
    }
  });
});

// 选择某种排序方式
$('.search-order').click(function () {
  $('.search-order').removeClass('active');
  $(this).addClass('active');
  $('#cur-order').text($(this).text());
});


<!-- 中间粘住检索结果 -->

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


<!-- 经目检索 -->

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
        return '<a href="/' + full[0] + '">' + full[0] + '</a>'
      }
    },
    {
      'targets': [1],
      'data': 'title',
      'render': function (data, type, full) {
        return '<a href="/' + full[0] + '">' + full[1] + '</a>'
      }
    },
  ]
});


<!-- 目录导航 -->

// 目录导航初始化
$(document).ready(function () {
  postApi('/cbeta/mulu', {'data': {'zang': zang, 'jing': jing}}, function (res) {
    var mulu_info = res.data;
    $('#my-mulu-tree').jstree({
      'core': {
        'data': mulu_info
      }
    });
  });
});

// 双击目录节点时，打开链接
$('#my-mulu-tree').bind("dblclick.jstree", function (event) {
  var node = $(event.target).closest("li");
  window.location = '/' + node.attr('title');
});