function obj_to_str(obj) {
    return [].concat(...(Object.values(obj))).join(', ');
}

function obj_arr_to_str(obj_arr) {
    return obj_arr.map(e => obj_to_str(e)).join(', ');
}

export {obj_to_str, obj_arr_to_str};