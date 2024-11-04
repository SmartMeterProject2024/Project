const JsonToVariables = require('../proxy')

describe('Convert JSON to Objects', () => {
  test('Should Convert a valid JSON Object', () => {
    const jsonObject = {id: 1234, time: "2024-10-29T21:07:28.484042", usage: 23.9};
    const expectedId = 1234
    const expectedTime = "2024-10-29T21:07:28.484042"
    const expectedUsage = 23.9
    const {id, time, usage} = JsonToVariables(jsonObject)
    expect(id).toEqual(expectedId)
    expect(time).toEqual(expectedTime)
    expect(usage).toEqual(expectedUsage)
  })
})