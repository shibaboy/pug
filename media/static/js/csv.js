(function($) {
	$.fn.exportAsCSV = function() {
		var error = this.attr("tagName") != "TABLE" && console && console.error("This function only supports TABLE tag.");
		if(error !== false) {
			return;
		}
		var csv = [];
		// header
		csv.push('"' + $("th", this).map(function() {
		  return $(this).text();
		}).get().join('","') + '"');
	        // body
		$("tr:gt(0)", this).each(function() {
			csv.push('"' + $("td", this).map(function() {
				return $(this).text();
			}).get().join('","') + '"');
		});
		location.href = "data:text/csv;charset=utf-8," + encodeURIComponent(csv.join("\r\n"));
		return this;
	}
})(jQuery);
