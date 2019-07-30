/*
 * cbeta.js
 *
 * Date: 2019-07-30
 */

<!-- 初始化 -->
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


<!-- 顶部导航第一行 -->

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

// 展开更多操作
$('.more .btn-more').click(function () {
  $('.more-group').toggleClass('hidden');
});

$('.more .btn-sm').click(function () {
  $(this).toggleClass('active');
});

// 显示行首
$('.more .btn-line-head').click(function () {
  if ($('#content-article').hasClass('article-row'))
    $('#content-article').removeClass('article-row').addClass('article');
  else
    $('#content-article').removeClass('article').addClass('article-row');
});

// 显示校勘
$('.more .btn-note').click(function () {
  if ($(this).hasClass('active')) {
    $('.content-left .note').hide();
  } else {
    $('.content-left .note').show();
    $('.content-left .note.mod').hide();
  }
});

// 显示标点
$('.more .btn-bd').click(function () {
  if ($(this).hasClass('active'))
    $('.content-left bd').hide();
  else
    $('.content-left bd').show();
});

$('.sub-line .order-wrap').click(function () {
  $('.search-orders').toggleClass('hide');
});

// 选择检索范围
$('.scope-item').click(function () {
  $('.scope-item').removeClass('active');
  $(this).addClass('active');
  $('#cur-scope').text($(this).text());
});


<!-- 顶部导航第二行 -->

// 增加字体
$('.sub-line .left .btn-font-enlarge').click(function () {
  var $article = $('.content > .content-left');
  var cur_size = parseFloat($article.css('font-size'));
  $article.css('font-size', cur_size + 1);
});

// 减少字体
$('.sub-line .left .btn-font-reduce').click(function () {
  var $article = $('.content > .content-left');
  var cur_size = parseFloat($article.css('font-size'));
  $article.css('font-size', cur_size - 1);
});

// 展开、收起顶部导航第二行
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

// 弹框-检索结果排序方式
$('.order-wrap').on('click', function (event) {
  event.stopPropagation();
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


<!-- 左侧文章阅读区域 -->

// 点击关键字，显示弹框
$('.kw').click(function (e) {
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

// 选中文字时，显示弹框
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


<!-- 中间粘住结果区域 -->
// 删除结果
$('.content-center .result-item .btn-operate').click(function () {
  $(this).parent().parent().remove();
});


<!-- 右侧检索结果区域 -->

// 粘住结果
$('.content-right .result-item .btn-operate').click(function () {
  $('.main-right .content .content-center').removeClass('hide');
  $('.m-header .sub-line .center').removeClass('hide');
  var item = $(this).parent().parent();
  item.find('.btn-operate').bind('click', function () {
    $(this).parent().parent().remove();
  });
  $('.content-center .result-items').append(item);
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
  $('#configModal .checkbox-inline').removeClass('active');
  $(this).addClass('active');
  $('.cur-search-scope').text($(this).text());
}

$('#configModal .checkbox-inline').bind('dblclick', dblClickCheckbox);

$('#configModal .add-search-scope').click(function () {
  var scopeStr = "<span class='search-scope'><input type='checkbox'/><label class='checkbox-inline' contenteditable='true'>新建</label></span>";
  $('#configModal .search-scope-groups').append(scopeStr);
  $('#configModal .search-scope-groups .checkbox-inline:last').focus();
  $('#configModal .checkbox-inline').unbind('dblclick').bind('dblclick', dblClickCheckbox);
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

// 经目检索-初始化
$('#my-sutra-table').DataTable({
  language: language,
  data: cbeta_sutras
});

function tableBind() {
  // 双击时阅读
  $('#my-table tbody tr').unbind('dblclick').dblclick(function () {
    var sutra_id = $(this).children().first().text();
    window.location = '/' + sutra_id;
  });
}

tableBind();

$('#my-sutra-table').DataTable().on('draw', function () {
  tableBind();
});


<!-- 目录导航 -->

// 双击目录节点时，打开链接
$('#my-mulu-tree').bind("dblclick.jstree", function (event) {
  var node = $(event.target).closest("li");
  window.location = '/' + node.attr('title');
});


