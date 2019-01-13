function getFitbitData() {

  return new Promise((resolve) => {
    let r = '{"data":{"success":true,"authorized":true,"data":{"competitions":[{"id":1,"name":"Workweek","points":54,"active_minutes":27,"cardio_zone_minutes":0,"peak_zone_minutes":0},{"id":4,"name":"Daily","points":54,"active_minutes":27,"cardio_zone_minutes":0,"peak_zone_minutes":0}],"errors":[]}}}'
    return setTimeout(() => resolve(JSON.parse(r)), 400)
  })
}


export { getFitbitData };
