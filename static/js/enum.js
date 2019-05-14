// Adapted from https://stackoverflow.com/a/24895217/1217464

// We're going to implement a basic enumeration prototype to generalize
// what you're looking for so you may re-use this code anywhere!
function Enum(valueMap) {
    // We store the enumeration object
    this._valueMap = valueMap;
    this._valueToLabelMap = {};
    var that = this;

    // This will create an inverse map: values to labels
    Object.keys(valueMap).forEach(function (label) {
        Object.defineProperty(that, label, {
            value: valueMap[label],
            writable: false
        });
        that._valueToLabelMap[valueMap[label]] = label;
    });
}

Enum.prototype = {
    // Getting the whole label is as simple as accessing
    // the inverse map where values are the object properties!
    getLabel: function (value) {
        if (this._valueToLabelMap.hasOwnProperty(value)) {
            return this._valueToLabelMap[value];
        } else {
            throw Error("Enum instance has no defined '" + value + "' value");
        }
    },
};