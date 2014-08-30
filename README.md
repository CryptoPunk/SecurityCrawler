SecurityCrawler

Crawl the web for fun stuff

Scrapers
* Implemented
 * HTML5
  * svg unimplemented due to confusion on xlink in html5
 * XHTML1.1 (partial)
  * TODO: Alert for unrecognized namespaces
 * Sitemap.xml (partial)
 * robots.txt

* Unimplemented
 * https://developer.mozilla.org/en-US/docs/XML_in_Mozilla
 * [Crossdomain.xml](http://www.adobe.com/devnet/articles/crossdomain_policy_file_spec.html)
 * [SVG](http://www.w3.org/TR/SVG)
 * PDF (Open that can of worms)
  * Xforms
  * Javascript
 * MS Office Files (Even worse, so many incompatable versions)
 * Open Office Files 
 * Flash
 * WSDL

* Crawler should use gevent.queue.JoinableQueue
