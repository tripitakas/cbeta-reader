<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:cb="http://www.cbeta.org/ns/1.0"
                xmlns:str="http://exslt.org/strings"
                extension-element-prefixes="str"
                xmlns:xs="http://www.w3.org/2001/XMLSchema"
                exclude-result-prefixes="xs cb">
  <xsl:output method="html" encoding="utf-8" doctype-system="about:legacy-compat" indent="yes"/>

  <!--当前经集的名字, 形如: T20n1167 -->
  <xsl:variable name="current_sutra" select="/TEI[1]/@xml:id"/>
  <xsl:variable name="current_book" select="substring-before($current_sutra, 'n')"/>  <!--XXX T20-->
  <!--xsl:variable name="current_juan" select="substring-after($current_sutra, 'n')"/--> <!---1167-->
  <xsl:variable name="title" select="substring-after(substring-after(/TEI/teiHeader/fileDesc/titleStmt/title, 'No. '), ' ')"/>
  <!--目录文件所在路径-->
  <xsl:variable name="toc_path" select="concat('/static/toc/', $current_book, '.toc')"/>
  <xsl:variable name="juan" select="format-number(/TEI/text/body//milestone[@unit='juan']/@n, '000')"/>
  <!--当前文件的语言, 默认繁体文言文-->
  <xsl:variable name="lang">
    <xsl:choose>
      <xsl:when test="/TEI/@xml:lang">
        <xsl:value-of select="/TEI/@xml:lang"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>lzh-Hant</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>
  <!--是否微软、火狐浏览器-->
  <xsl:variable name="MSIE" select="system-property('xsl:vendor')='Microsoft'"/>
  <xsl:variable name="firefox" select="system-property('xsl:vendor')='Transformiix'"/>
  <!--版权-->
  <xsl:variable name="copyright">
    <xsl:choose>
      <xsl:when test="starts-with($current_sutra, 'T')">
        <xsl:text>《大正新脩大藏經》（大藏出版株式會社 ©）</xsl:text>
      </xsl:when>
      <xsl:when test="starts-with($current_sutra, 'X')">
        <xsl:text>《卍新纂續藏經》（株式會社國書刊行會 ©）</xsl:text>
      </xsl:when>
      <xsl:when test="starts-with($current_sutra, 'A')">
        <xsl:text>《趙城金藏》</xsl:text>
      </xsl:when>
      <xsl:when test="starts-with($current_sutra, 'C')">
        <xsl:text>《中華藏》</xsl:text>
      </xsl:when>
      <xsl:when test="starts-with($current_sutra, 'F')">
        <xsl:text>《房山石經》</xsl:text>
      </xsl:when>
      <xsl:when test="starts-with($current_sutra, 'J')">
        <xsl:text>《嘉興大藏經》（新文豐出版公司）</xsl:text>
      </xsl:when>
      <xsl:when test="starts-with($current_sutra, 'K')">
        <xsl:text>《高麗藏》（新文豐出版公司）</xsl:text>
      </xsl:when>
      <xsl:when test="starts-with($current_sutra, 'L')">
        <xsl:text>《乾隆藏》</xsl:text>
      </xsl:when>
      <xsl:when test="starts-with($current_sutra, 'M')">
        <xsl:text>《卍正藏經》（新文豐出版公司）</xsl:text>
      </xsl:when>
      <xsl:when test="starts-with($current_sutra, 'P')">
        <xsl:text>《永樂北藏》</xsl:text>
      </xsl:when>
      <xsl:when test="starts-with($current_sutra, 'S')">
        <xsl:text>《宋藏遺珍》</xsl:text>
      </xsl:when>
      <xsl:when test="starts-with($current_sutra, 'U')">
        <xsl:text>《洪武南藏》</xsl:text>
      </xsl:when>
      <xsl:when test="starts-with($current_sutra, 'D')">
        <xsl:text>國家圖書館善本佛典</xsl:text>
      </xsl:when>
      <xsl:when test="starts-with($current_sutra, 'N')">
        <xsl:text>《漢譯南傳大藏經》（元亨寺 ©）</xsl:text>
      </xsl:when>
      <xsl:when test="starts-with($current_sutra, 'I')">
        <xsl:text>《北朝佛教石刻拓片百品》（中央研究院歷史語言研究所 ©）</xsl:text>
      </xsl:when>
      <xsl:when test="starts-with($current_sutra, 'ZW')">
        <xsl:text>《藏外佛教文獻》（方廣錩 ©）</xsl:text>
      </xsl:when>
      <xsl:when test="starts-with($current_sutra, 'GA')">
        <xsl:text>《中國佛寺史志彙刊》（杜潔祥主編）</xsl:text>
      </xsl:when>
      <xsl:when test="starts-with($current_sutra, 'ZW')">
        <xsl:text>《藏外佛教文獻》（方廣錩 ©）</xsl:text>
      </xsl:when>
      <xsl:when test="starts-with($current_sutra, 'GB')">
        <xsl:text>《中國佛寺志叢刊》（張智等編輯）</xsl:text>
      </xsl:when>
      <xsl:when test="starts-with($current_sutra, 'Y')">
        <xsl:text>《印順法師佛學著作集》（印順文教基金會©）</xsl:text>
      </xsl:when>
      <xsl:when test="starts-with($current_sutra, 'G')">
        <xsl:text>《佛教大藏經》</xsl:text>
      </xsl:when>
    </xsl:choose>
  </xsl:variable>
  <!--xml所在目录前缀, 形如: /xml/T01/-->
  <xsl:variable name="dir" select="concat('/xml/', substring-before($current_sutra, 'n'), '/')"/>

  <!--开始页面根元素: 默认使用繁体文言文-->
  <xsl:template match="/">
    <html lang="{$lang}">
      <head>
        <link rel="stylesheet" href="/static/css/tei.css?v=04425bbdc6243fc6e54bf8984fe50330"/>
      </head>
      <body>
        <div class="contentx">
          <xsl:apply-templates/>
        </div>
        <div class="copyright">【經文資訊】
          <xsl:value-of select="$copyright"/>
          第
          <xsl:value-of select="concat(substring-before($current_sutra, 'n'), ' 冊 No. ', substring-after($current_sutra, 'n'), ' ', $title)"/>
          <br/>
          【原始資料】
          <xsl:value-of select="/TEI/teiHeader/encodingDesc/projectDesc/p[@xml:lang='zh-Hant']"/>
          <br/>
          【其他事項】本資料庫可自由免費流通，詳細內容請參閱【中華電子佛典協會資料庫版權宣告】
        </div>
      </body>
    </html>
  </xsl:template>


  <xsl:template match="teiHeader"/>

  <xsl:template match="text/body/cb:docNumber">
    <span class="doc-number">
      <xsl:apply-templates/>
    </span>

  </xsl:template>

  <!--不显示back部分-->
  <xsl:template match="text/back">
  </xsl:template>

  <!--不能切换段落, 否则显示不正常-->
  <xsl:template match="pb">
  </xsl:template>

  <!--不在正文显示目录-->
  <xsl:template match="cb:mulu">
    <a class="mulu">
      <xsl:attribute name="id">
        <xsl:value-of select="generate-id()"/>
      </xsl:attribute>
    </a>
  </xsl:template>

  <!--处理表格table-->
  <!--TODO: table rend="border:0"-->
  <xsl:template match="table">
    <table class="table table-bordered">
      <xsl:apply-templates/>
    </table>
  </xsl:template>

  <!--处理表格row-->
  <xsl:template match="row">
    <tr>
      <xsl:apply-templates/>
    </tr>
  </xsl:template>

  <!--处理表格cell FIXME: firefox表格錯位-->
  <xsl:template match="cell">
    <td>
      <xsl:if test="@cols">
        <xsl:attribute name="colspan">
          <xsl:value-of select="@cols"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:if test="@rows">
        <xsl:attribute name="rowspan">
          <!--xsl:if test="$firefox">
          <xsl:value-of select="@rows+1"/>
          </xsl:if>
          <xsl:if test="not($firefox)"-->
          <xsl:value-of select="@rows"/>
          <!--/xsl:if-->
        </xsl:attribute>
      </xsl:if>
      <xsl:apply-templates/>
    </td>
  </xsl:template>

  <!--处理所有的颂-->
  <!-- rend="margin-left:1em;text-indent:-1em" -->
  <xsl:template match="lg">
    <div class="lg">
      <xsl:if test="@xml:id">
        <xsl:attribute name="id">
          <xsl:value-of select="@xml:id"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:attribute name="class">
        <xsl:choose>
          <xsl:when test="starts-with(child::l[1], '「『')">
            <xsl:text>lll</xsl:text>
          </xsl:when>
          <xsl:when
              test="starts-with(child::l[1], '「') or starts-with(child::l[1], '“') or starts-with(child::l[1], '∴')">
            <xsl:text>ll</xsl:text>
          </xsl:when>
          <xsl:otherwise>
            <xsl:text>lg</xsl:text>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:attribute>
      <!--xsl:choose>
          <xsl:when test="@rend">
              <xsl:attribute name="style">
              <xsl:value-of select="concat('text-indent:', substring-before(substring-after(@rend,'text-indent:'), 'em'), 'em;')"/>
              </xsl:attribute>
          </xsl:when>
          <xsl:otherwise>
          </xsl:otherwise>
      </xsl:choose-->
      <xsl:apply-templates/>
    </div>
  </xsl:template>

  <!--偈中重复的换行只显示一个换行-->
  <xsl:template match="lg/lb">
    <xsl:if test="local-name(preceding-sibling::*[1])!='lb'">
      <br/>
    </xsl:if>
  </xsl:template>

  <xsl:template match="lb">
    <span class="lb">
      <xsl:value-of select="concat($current_sutra, '_', @n, ':')"/>
    </span>
  </xsl:template>

  <xsl:template match="lg/l">
    <span class="l">
      <xsl:apply-templates/>
    </span>
  </xsl:template>

  <!--清除文档中无用空格, 替换错误的人名分割符号-->
  <xsl:template match="text()|@*">
    <xsl:value-of select="normalize-space(.)"/>
  </xsl:template>

  <!--处理图片-->
  <xsl:template match="figure">
    <figure>
      <xsl:apply-templates/>
      <figcaption>
        <xsl:value-of select="head"/>
      </figcaption>
    </figure>
  </xsl:template>

  <xsl:template match="graphic">
    <img class="img-responsive">
      <xsl:attribute name="src">
        <xsl:text>/static</xsl:text>
        <xsl:value-of select="substring(@url, 3)"/>
      </xsl:attribute>
    </img>
  </xsl:template>

  <!--处理段落-->
  <!--xsl:template match="p[contains(@rend, 'inline')]">
      <span><xsl:apply-templates/></span>
  </xsl:template-->

  <!--xsl:template match="p[@cb:type='dharani']/lb">
      <xsl:if test="local-name(preceding-sibling::*[1])!='lb'">
          <br/>
      </xsl:if>
  </xsl:template-->

  <xsl:template match="p[contains(@cb:type, 'head')]">
    <xsl:variable name="hunit" select="concat('h', substring(@cb:type, 5)+1)"/>
    <xsl:element name="{$hunit}">
      <xsl:apply-templates/>
    </xsl:element>
  </xsl:template>

  <!--咒语段落, 分成悉昙体和汉语两个段落表现 -->
  <!--xsl:template match="p[@cb:type='dharani']">
      <p class="dharani">
          <xsl:apply-templates/>
      </p>
  </xsl:template-->

  <!--XXX-->
  <xsl:template match="cb:t[@xml:lang='zh-x-yy']">
    [<xsl:apply-templates/>]
  </xsl:template>

  <xsl:template match="p[@cb:type='dharani']">
    <xsl:choose>
      <xsl:when test="not(cb:tt)">
        <p class="dharani">
          <xsl:apply-templates/>
        </p>
      </xsl:when>
      <xsl:when test="cb:tt[@place='inline']">
        <p class="dharani">
          <span lang="sa-Sidd">
            <xsl:apply-templates select="cb:tt/cb:t[@xml:lang='sa-Sidd']"/>
          </span>
          <!--span lang="sa-Sidd"><xsl:apply-templates select="starts-with(cb:tt/cb:t[@xml:lang], 'sa')"/></span-->
          <!--span lang="sa-x-rj"><xsl:apply-templates select="cb:tt/cb:t[@xml:lang='sa-x-rj']"/></span-->
          <span lang="zh-Hant">(<xsl:apply-templates select="cb:tt/cb:t[@xml:lang='zh-Hant']"/>)
          </span>
          <!--span lang="zh-Hant">(<xsl:apply-templates select="starts-with(cb:tt/cb:t[@xml:lang], 'zh')"/>)</span-->
          <!--span lang="zh-Hant">(<xsl:apply-templates select="cb:tt/cb:t[@xml:lang='zh-x-yy']"/>)</span-->
          <xsl:apply-templates/>
        </p>
      </xsl:when>
      <xsl:otherwise>
        <p lang="sa-Sidd" class="dharani">
          <xsl:apply-templates select="cb:tt/cb:t[@xml:lang='sa-Sidd']"/>
        </p>
        <!--p lang="sa-x-rj" class="dharani"><xsl:apply-templates select="cb:tt/cb:t[@xml:lang='sa-x-rj']"/></p-->
        <p lang="zh-Hant" class="dharani">
          <xsl:apply-templates select="cb:tt/cb:t[@xml:lang='zh-Hant']"/>
        </p>
        <!--p lang="zh-Hant" class="dharani"><xsl:apply-templates select="cb:tt/cb:t[@xml:lang='zh-x-yy']"/></p-->
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="p[@cb:type='pre']">
    <pre>
      <xsl:value-of select="."/>
    </pre>
  </xsl:template>

  <xsl:template match="p">
    <p lang="lzh-Hant">
      <xsl:if test="@xml:id">
        <xsl:attribute name="id">
          <xsl:value-of select="@xml:id"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:apply-templates/>
    </p>
  </xsl:template>

  <!--处理词典-->
  <xsl:template match="entry">
    <dl>
      <xsl:apply-templates/>
    </dl>
  </xsl:template>
  <xsl:template match="form">
    <dt>
      <xsl:apply-templates/>
    </dt>
  </xsl:template>
  <xsl:template match="cb:def">
    <dd>
      <xsl:apply-templates/>
    </dd>
  </xsl:template>

  <!--处理note-->
  <xsl:template match="note[@place='inline']|note[@type='inline']">
    <span lang="lzh-Hant" class="note">(<xsl:apply-templates/>)
    </span>
  </xsl:template>

  <xsl:template match="space">
    <span style="display:inline-block">
      <xsl:if test="@quantity">
        <xsl:variable name="unit">
          <xsl:choose>
            <xsl:when test="@unit='chars'">
              <xsl:text>em</xsl:text>
            </xsl:when>
            <xsl:when test="@unit">
              <xsl:value-of select="@unit"/>
            </xsl:when>
            <xsl:otherwise>em</xsl:otherwise>
          </xsl:choose>
        </xsl:variable>
        <xsl:attribute name="width">
          <xsl:value-of select="@quantity"/>
          <xsl:value-of select="$unit"/>
        </xsl:attribute>
      </xsl:if>
    </span>
  </xsl:template>

  <!--处理teiHeader-->
  <xsl:template match="titleStmt/title">
    <xsl:if test="preceding-sibling::title">
      <br/>
    </xsl:if>
    <xsl:apply-templates/>
  </xsl:template>

  <!--head 小节的目录。上级节点是div类节点则不显示? -->
  <xsl:template match="head">
    <xsl:variable name="parent" select="local-name(..)"/>
    <!--xsl:if test="not(starts-with($parent,'div'))">
      <xsl:apply-templates/>
    </xsl:if-->
    <h2 class="head">
      <xsl:apply-templates/>
    </h2>
  </xsl:template>

  <!--标题 type=X, pin-->
  <xsl:template match="cb:jhead">
    <h1 class="title">
      <xsl:apply-templates/>
    </h1>
    <!--br/-->
  </xsl:template>

  <!--最后一个作者译者cb:type="author"之后空出两行然后开始正文-->
  <xsl:template match="byline">
    <div class="byline">
      <xsl:apply-templates/>
    </div>
    <xsl:if test="../byline[last()]=.">
      <br/>
    </xsl:if>
  </xsl:template>

  <!--列表中的作者译者不另外换行,应该清洗掉这种标志 XXX-->
  <xsl:template match="list//byline|cb:jl_byline">
    <span class="byline">
      <xsl:apply-templates/>
    </span>
  </xsl:template>

  <!--处理列表-->
  <xsl:template match="list">
    <ul>
      <xsl:apply-templates/>
    </ul>
  </xsl:template>
  <xsl:template match="list/item">
    <li>
      <xsl:apply-templates/>
    </li>
  </xsl:template>

  <!--处理空缺 unclear@reason-->
  <xsl:template match="unclear">
    <span class="unclear">
      <xsl:text>&#x258a;</xsl:text>
    </span>
  </xsl:template>

  <!--使用popover显示注释, 链接三个标签，可能有些不对 TODO 使用超链接-->
  <!--跨文件注释？note type="cf1">K19n0663_p0486b18</note-->
  <xsl:template match="note[starts-with(@type, 'cf')]">
    (見:
    <a>
      <xsl:value-of select="."/>
    </a>
    )
  </xsl:template>
  <!--xsl:template match="reg">
  </xsl:template-->

  <xsl:template match="orig">
    <xsl:apply-templates/>
    <xsl:text>&#8658;</xsl:text>
  </xsl:template>

  <!--lem是版本, corr是勘误-->
  <xsl:template match="lem|corr">
    <xsl:apply-templates/>
    <xsl:if test="@wit">
      <xsl:call-template name="tokenize">
        <xsl:with-param name="string" select="@wit"/>
      </xsl:call-template>
    </xsl:if>
    <xsl:text>&#8656;</xsl:text>
  </xsl:template>

  <xsl:template match="rdg|sic">
    <xsl:apply-templates/>
    <xsl:if test="@wit">
      <xsl:call-template name="tokenize">
        <xsl:with-param name="string" select="@wit"/>
      </xsl:call-template>
    </xsl:if>
  </xsl:template>

  <!--比较危险的用法,可能报错: 给替换的部分着红色-->

  <xsl:key name="tt_from" match="cb:tt" use="@from"/>
  <xsl:key name="app_from" match="app" use="@from"/>
  <xsl:key name="choice_from" match="choice" use="@cb:from"/>
  <xsl:key name="note_target" match="note" use="@target"/>
  <xsl:key name="note_n" match="note" use="@n"/>
  <xsl:key name="witness_id" match="witness" use="@xml:id"/>

  <xsl:template match="anchor">
    <xsl:variable name="Ref" select="concat('#', @xml:id)"/>
    <!--注释使用花青色-->
    <xsl:if test="not($firefox) and starts-with(@xml:id, 'beg')">
      <xsl:text disable-output-escaping="yes">&lt;span></xsl:text>
    </xsl:if>
    <xsl:if test="not($firefox) and starts-with(@xml:id, 'end')">
      <xsl:text disable-output-escaping="yes">&lt;/span&gt;</xsl:text>
    </xsl:if>
    <sup lang="en" class="note">
      <span data-toggle="popover" data-placement="auto" data-container="body" data-trigger="focus hover" data-delay="500">
        <xsl:if test="@xml:id">
          <xsl:attribute name="id">
            <xsl:value-of select="@xml:id"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:attribute name="class">
          <xsl:value-of select="key('note_target', $Ref)/@type"/>
        </xsl:attribute>
        <xsl:choose>
          <xsl:when test="@type='cb-app' and key('app_from', $Ref)">
            <xsl:attribute name="data-title">
              <xsl:value-of select="key('app_from', $Ref)/../../head"></xsl:value-of>
            </xsl:attribute>
            <xsl:attribute name="data-content">
              <xsl:apply-templates select="key('app_from', $Ref)"/>
            </xsl:attribute>
            <xsl:value-of select="concat('[c', substring(@xml:id, 5), ']')"/>
          </xsl:when>
          <xsl:when test="@type='cb-app' and key('choice_from', $Ref)/sic">
            <xsl:attribute name="data-title">
              <xsl:value-of select="key('choice_from', $Ref)/../../head"></xsl:value-of>
            </xsl:attribute>
            <xsl:attribute name="data-content">
              原文為:
              <xsl:apply-templates select="key('choice_from', $Ref)/sic"/>
            </xsl:attribute>
            <xsl:value-of select="concat('[c', substring(@xml:id, 5), ']')"/>
          </xsl:when>
          <xsl:when test="@type='cb-app' and key('choice_from', $Ref)/reg">
            <xsl:attribute name="data-title">
              <xsl:apply-templates select="key('choice_from', $Ref)/reg/@type"/>  <!--通用詞-->
            </xsl:attribute>
            <xsl:attribute name="data-content">
              <xsl:apply-templates select="key('choice_from', $Ref)"/>
            </xsl:attribute>
            <xsl:value-of select="concat('[c', substring(@xml:id, 5), ']')"/>
          </xsl:when>
          <xsl:when test="@type='star' and key('app_from', $Ref)">
            <xsl:attribute name="data-title">
              <!--xsl:text>註解</xsl:text-->
              <xsl:value-of select="key('app_from', $Ref)/../../head"></xsl:value-of>
            </xsl:attribute>
            <xsl:attribute name="data-content">
              <xsl:apply-templates select="key('app_from', $Ref)"/>,
              <!--xsl:variable name="tmp" select="substring(key('app_from', $Ref)/@corresp, 2)"/>
              <xsl:apply-templates select="key('note_n', $tmp)"/-->
            </xsl:attribute>
            <xsl:text>[*]</xsl:text>
          </xsl:when>
          <xsl:when test="key('note_target', $Ref)">
            <xsl:attribute name="data-title">
              <!--xsl:text>註釋xx</xsl:text-->
              <xsl:value-of select="key('note_target', $Ref)/../../head"></xsl:value-of>
            </xsl:attribute>
            <xsl:attribute name="data-content">
              <xsl:apply-templates select="key('note_target', $Ref)"/>
            </xsl:attribute>
            <xsl:value-of select="concat('[', substring(@n, 6), ']')"/>
          </xsl:when>
          <xsl:when test="@type='circle'">
          </xsl:when>
        </xsl:choose>
      </span>
    </sup>
  </xsl:template>


  <!--处理div 折叠式注释 TODO, 里面的异体字处理有些问题D47n8936_002-->
  <!--xsl:template match="cb:div[@type='orig']"-->
  <xsl:template match="cb:div[@type='commentary']">
    <div class="commentary panel-collapse">
      <a data-toggle="collapse" data-parent="#accordion" href="#{generate-id()}"><span class="caret"/>註疏：
      </a>
      <div id="{generate-id()}" class="panel-collapse collapse">
        <div class="panel-body">
          <xsl:apply-templates/>
        </div>
      </div>
    </div>
    <br/>
  </xsl:template>


  <!--生成导航目录 max(cb:mulu@level)=28, XXX: 不能显示cb:mulu中的异体字:K34n1257_007.xml-->
  <xsl:template name="make_catalog">
    <xsl:param name="pos"/>
    <xsl:for-each select="$pos">
      <xsl:choose>
        <xsl:when test="@level=1">
          <li class="toc">
            <a>
              <xsl:attribute name="href">
                <xsl:text>#</xsl:text>
                <xsl:value-of select="following::*[@xml:id][1]/@xml:id"/>
              </xsl:attribute>
              <xsl:value-of select="."/>
            </a>
          </li>
        </xsl:when>
        <xsl:when test="@level=2">
          <ul>
            <li>
              <a>
                <xsl:attribute name="href">
                  <xsl:text>#</xsl:text>
                  <xsl:value-of select="following::*[@xml:id][1]/@xml:id"/>
                </xsl:attribute>
                <xsl:value-of select="."/>
              </a>
            </li>
          </ul>
        </xsl:when>
        <xsl:when test="@level=3">
          <ul>
            <ul>
              <li>
                <a>
                  <xsl:attribute name="href">
                    <xsl:text>#</xsl:text>
                    <xsl:value-of select="following::*[@xml:id][1]/@xml:id"/>
                  </xsl:attribute>
                  <xsl:value-of select="."/>
                </a>
              </li>
            </ul>
          </ul>
        </xsl:when>
        <xsl:when test="@level=4">
          <ul>
            <ul>
              <ul>
                <li>
                  <a>
                    <xsl:attribute name="href">
                      <xsl:text>#</xsl:text>
                      <xsl:value-of select="following::*[@xml:id][1]/@xml:id"/>
                    </xsl:attribute>
                    <!--xsl:apply-templates select="."/-->
                    <!--xsl:copy-of select="."/-->
                    <xsl:value-of select="."/>
                  </a>
                </li>
              </ul>
            </ul>
          </ul>
        </xsl:when>
      </xsl:choose>
    </xsl:for-each>
  </xsl:template>

  <!--cb:yin><cb:zi>得浪</cb:zi><cb:sg>二合</cb:sg></cb:yin-->
  <xsl:template match="cb:sg">(<xsl:apply-templates/>)
  </xsl:template>

  <!--公式强调角标-->
  <xsl:template match="hi">
    <span class="formula">
      <xsl:if test="@rend">
        <xsl:attribute name="style">
          <xsl:value-of select="@rend"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:apply-templates/>
    </span>
  </xsl:template>


  <!-- <ref target="#PTS.Ja.3.227" type="PTS_hide"> -->
  <!-- <ref target="#PTS.Ja.3.153"> -->
  <!-- <ref cRef="PTS.Ja.1.1"/> -->
  <!-- <ref target="../T31/T31n1585.xml#xpath2(//0041b09)"> -->
  <!-- <ref target="../T31/T31n1585_008.xml#0041b09)"> TODO -->
  <xsl:template match="ref">
    <a>
      <xsl:attribute name="href">
        <!--xsl:value-of select="concat($current_sutra, '_p', @n)" /-->
        <xsl:if test="@target">
          <xsl:value-of select="@target"/>
        </xsl:if>
        <xsl:if test="@cRef">
          <xsl:value-of select="@cRef"/>
        </xsl:if>
      </xsl:attribute>
      <!--xsl:value-of select="."/-->
      <xsl:choose>
        <xsl:when test="not(text())">
          <sup lang="en">[pts]</sup>
        </xsl:when>
        <xsl:otherwise>
          <xsl:apply-templates/>
        </xsl:otherwise>
      </xsl:choose>
    </a>
  </xsl:template>

  <!-- <term rend="no_nor"> 此标签内的g不规范化-->
  <xsl:template match="term">
    <dfn class="term">
      <xsl:apply-templates/>
    </dfn>
  </xsl:template>

  <!--'sa-x-rj', 'en', 'sa-Sidd', 'zh', 'san-tr', 'sa', 'x-unknown', 'pi', 'zh-x-yy'-->
  <!--sa, pi, x-unknown-->
  <xsl:template match="foreign">
    <!--span>
        <xsl:attribute name="lang">
          <xsl:value-of select="@xml:lang"/>
        </xsl:attribute>
    </span-->
    <xsl:choose>
      <xsl:when test="@xml:lang='sa'">
        <xsl:text>[梵語]</xsl:text>
        <xsl:apply-templates/>
      </xsl:when>
      <xsl:when test="@xml:lang='pi'">
        <xsl:text>[巴利語]</xsl:text>
        <xsl:apply-templates/>
      </xsl:when>
      <xsl:when test="@xml:lang='x-unknown'">
        <xsl:text>[UNKNOWN]</xsl:text>
        <xsl:apply-templates/>
      </xsl:when>
    </xsl:choose>
  </xsl:template>

  <!-- 经录的卷数 -->
  <xsl:template match="cb:jl_juan">
    <span class="jl">
      <xsl:apply-templates/>
    </span>
  </xsl:template>

  <!-- 经录的标题: TODO 做一个超链接到应该的文件 -->
  <xsl:template match="cb:jl_title|item/title">
    <cite>
      <a>
        <xsl:attribute name="href">
          <xsl:text>/searchmulu?title=</xsl:text>
          <xsl:apply-templates/>   <!--TODO 应该去掉这里的注释-->
        </xsl:attribute>
        <xsl:apply-templates/>
      </a>
    </cite>
  </xsl:template>

  <!--敬语-->
  <xsl:template match="persName">
    <span class="honorific">
      <xsl:apply-templates/>
    </span>
  </xsl:template>

  <!--string-split函数: 空格分割后取值witness@id-->
  <xsl:template match="text/text()" name="tokenize">
    <xsl:param name="string" select="."/>
    <xsl:param name="delimiters" select="' '"/>
    <xsl:choose>
      <xsl:when test="not(contains($string, $delimiters))">
        <xsl:value-of select="key('witness_id', substring(normalize-space($string), 2))"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of
            select="key('witness_id', substring(normalize-space(substring-before($string, $delimiters)), 2))"/>
        <xsl:call-template name="tokenize">
          <xsl:with-param name="string" select="substring-after($string, $delimiters)"/>
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!--注音模板, 使用kx.xml作为字典给全文注音-->
  <!--xsl:template match="text/text()" name="zhuyin">
      <xsl:param name="string" select="."/>
      <xsl:param name="num" select="1"/>
              <xsl:variable name="zi" select="substring($string, $num, 1)"/>
              <ruby>
                  <xsl:value-of select="substring($string, $num, 1)"/>
                  <rt>
                      <xsl:value-of select="document('kx.xml')//char[@zi=$zi]"/>
                  </rt>
              </ruby>
          <xsl:if test="substring($string, $num+1, 1)">
              <xsl:call-template name="zhuyin">
                  <xsl:with-param name="string" select="substring($string, $num+1)"/>
              </xsl:call-template>
          </xsl:if>
  </xsl:template-->

  <!--计数循环-->
  <xsl:template name="loop">
    <xsl:param name="Count"/>
    <xsl:if test="$Count&lt;1">
      <xsl:value-of select="'finish'"/>
    </xsl:if>
    <xsl:if test="$Count&gt;=1">
      <xsl:value-of select="$Count"/>
      <xsl:call-template name="loop">
        <xsl:with-param name="Count">
          <xsl:value-of select="number($Count)-1"/>
        </xsl:with-param>
      </xsl:call-template>
    </xsl:if>
  </xsl:template>

</xsl:stylesheet>

