// Function to convert JSON object into variables
function JsonToVariables(jsonObject) {
  const { id, time, usage } = jsonObject;
  return { id, time, usage };
}
module.exports = JsonToVariables;