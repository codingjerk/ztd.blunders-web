var grid = {};

(function (module) {
    var generateCaption = function(caption) {
        return '<tr class="caption-row"><td class="caption-block" colspan="3">{0}</td></tr>'
            .format(caption);
    }

    var generateNamedRow = function(rowData) {
        return '<tr class="info-row"><td class="info-block-wrapper" colspan="3"><div id="{0}"></div></td></tr>'
            .format(rowData.id);
    }

    var generateCell = function(cell) {
        return ('<td class="grid-block">' +
            '<div class="grid-label">{0}</div>' +
            '<div class="grid-value" id="{1}"></div>' +
            '<div class="grid-additional">{2}</div>' +
            '</td>').format(cell.label, cell.id, cell.additional);
    }

    var generateRow = function(rowData) {
        if (rowData.type === 'cell') {
            return generateCell(rowData);
        } else if (rowData.type === 'chart') {
            return generateNamedRow(rowData);
        }

        console.log('Unknown row type');
    }

    var parseNamedRows = function(rowsData) {
        var result = '';

        while (rowsData.length > 0) {
            if (rowsData[0].type !== 'chart') break;

            var rowData = rowsData.shift();
            result += generateRow(rowData);
        }

        return result;
    }

    var parseCells = function(rowsData) {
        var cells = [];

        while (rowsData.length > 0) {
            if (rowsData[0].type !== 'cell') break;

            var rowData = rowsData.shift();
            cells.push(generateRow(rowData));
        }

        var result = '';

        while (cells.length > 0) {
            var c1 = cells.shift() || '';
            var c2 = cells.shift() || '';
            var c3 = cells.shift() || '';

            result += '<tr class="grid-row">{0}{1}{2}</tr>'.format(c1, c2, c3);
        }

        return result;
    }

    var generateRows = function(rowsData) {
        var result = '';

        while (rowsData.length > 0) {
            result += parseNamedRows(rowsData);
            result += parseCells(rowsData);
        }

        return result;
    }

    var generateBlock = function(block) {
        var caption = generateCaption(block.caption);
        var body = generateRows(block.rows);

        return '<table class="details-block">{0}{1}</table>'.format(caption, body);
    }

    module.generate = function(blocks) {
        var result = '';

        blocks.forEach(function(block) {
            result += generateBlock(block);
        });

        return result;
    }

    module.update = function(data, rules) {
        for (var i = 0; i < data.length; i++) {
            var element = data[i];

            var ruleFunction = rules[element.id];
            if (ruleFunction !== undefined) {
                ruleFunction(element);
            } else {
                $('#' + element.id).html(element);
            }
        }
    }
})(grid);