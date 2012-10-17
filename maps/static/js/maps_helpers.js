var hittest_data = [];
var hittest_data_loading = false;
function map_hit_test(coord, layer, boundary, callback, api_root) {
	if (hittest_data_loading) return;
	hittest_data_loading = true;
	
	var data_key = layer + "/" + (boundary ? boundary : "") + "/" + coord.zoom + "/" + coord.tile_x + "/" + coord.tile_y;
	for (var i = 0; i < hittest_data.length; i++) {
		if (hittest_data[i].key == data_key) {
			map_hit_test_2(coord, hittest_data[i].value, callback)
			hittest_data_loading = false;
			return;
		}
	}
	
	// pop the oldest tile
	if (hittest_data.length > 32) hittest_data.shift();
	
	var format = (!api_root ? 'json' : 'jsonp');
	$.ajax(
		(api_root ? api_root : "") + "/map/tiles/" + layer + (boundary ? "/" + boundary : "") + "/" + coord.zoom + "/" + coord.tile_x + "/" + coord.tile_y + "." + format,
		{
			dataType: format,
			cache: true,
			success: function(data) {
				hittest_data.push({ key: data_key, value: data });
				map_hit_test_2(coord, data , callback);
 			},
			complete: function(xhr, textstatus) {
				hittest_data_loading = false;
			}
		}
	);
}
function map_hit_test_2(coord, grid_data, callback) {
	if (!grid_data.grid) {
		callback(null, null);
		return;
	}
	var grid_size = grid_data.grid.length;
	var x = Math.floor(coord.offset_x / 256 * grid_size);
	var y = Math.floor(coord.offset_y / 256 * grid_size);
	var b = grid_data.grid[y].charCodeAt(x);
	if (b >= 93) b--;
	if (b >= 35) b--;
	b -= 32;
	var key = grid_data.keys[b];
	callback(key, grid_data.data ? grid_data.data[key] : null);
}

