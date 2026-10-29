# frozen_string_literal: true

# `bust_css_cache` (jekyll-cache-bust, patched by al_folio_core) builds main.css?v= from the
# theme gem's _sass only, so edits to this site's _sass/ (e.g. _custom.scss) keep the same URL
# and browsers like Safari keep serving the cached stylesheet. Fold the site's partials into the
# digest. _plugins load after gems, so this wraps al_folio_core's patch and calls through to it.
module SiteSassCacheBust
  SITE_SASS_GLOB = File.join("_sass", "**", "*")

  private

  def directory_files_content
    site_sass = Dir[SITE_SASS_GLOB].sort.select { |f| File.file?(f) }.map { |f| File.read(f) }.join
    super + site_sass
  end
end

if defined?(Jekyll::CacheBust::CacheDigester) && !Jekyll::CacheBust::CacheDigester.ancestors.include?(SiteSassCacheBust)
  Jekyll::CacheBust::CacheDigester.prepend(SiteSassCacheBust)
end
