from phase1.seed_sos import county_key, parse_links, parse_officials

NORMAL = """<dl>
      <dt><strong><a name="A" id="A"></a>ANDERSON COUNTY</strong></dt>
      <dd>Elections Administrator</dd>
      <dd>Casey Brown</dd>
      <dd>703 N. Mallard St., Ste 116 Palestine 75801 </dd>
      <dd><a href="mailto:cbrown@co.anderson.tx.us" title="Anderson County">County Email Address</a></dd>
      <dd>(903) 723-7438</dd>
      <dd>FAX: (903) 723-1223</dd>
      <dd><a href="mailto:electionsclerk@co.anderson.tx.us" title="x">Submit your Application for Ballot By Mail</a></dd>    </dl>"""

PACKED = """<dl>
      <dt><strong>BURNET COUNTY</strong></dt>
      <dd>Elections Administrator</dd>
      <dd>Stephanie Cooper</dd>
      <dd>106 W. Washington St., Burnet, 78611 <br />
        Mailing address: 220 S. Pierce St., Burnet 78611 <br />
  <a href="mailto:elections@burnetcountytexas.org" title="Burnet County">County Email Address<br />
  </a>(512) 715-5288<br />
        FAX: (512) 715-5287<br />
  <a href="mailto:elections@burnetcountytexas.org" title="x">Submit your Application for Ballot By Mail</a></dd>
      <dt>&nbsp;</dt>
    </dl>"""


def test_normal_entry():
    (e,) = parse_officials(NORMAL)
    assert e["county"] == "Anderson" and e["office_title"] == "Elections Administrator"
    assert e["official"] == "Casey Brown" and e["phone"] == "(903) 723-7438"
    assert e["email"] == "cbrown@co.anderson.tx.us" and e["abbm_email"] == "electionsclerk@co.anderson.tx.us"
    assert e["fax"] == "(903) 723-1223"


def test_packed_entry():
    (e,) = parse_officials(PACKED)
    assert e["county"] == "Burnet" and e["phone"] == "(512) 715-5288"
    assert e["email"] == "elections@burnetcountytexas.org" and e["fax"] == "(512) 715-5287"
    assert e["address"][0].startswith("106 W. Washington")


def test_county_names():
    assert county_key("MCLENNAN COUNTY") == "McLennan"
    assert county_key("DE WITT COUNTY") == "DeWitt"
    assert county_key("JIM  HOGG COUNTY") == "Jim Hogg"


def test_links_decode_entities():
    page = '<a name="County"></a><td><a href="http://x.gov/?a=1&amp;b=2">Red  River County</a></td>'
    assert parse_links(page) == {"Red River": "http://x.gov/?a=1&b=2"}
