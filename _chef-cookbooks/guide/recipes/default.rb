execute "apt-get-update" do
  command "apt-get update"
  ignore_failure true
end

package "python-jinja2"
package "ruby-sass"
package "inkscape"
package "graphicsmagick"
package "optipng"
package "pngquant"
package "python-scour"
package "python-html5lib"
