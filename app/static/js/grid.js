var grid = {};

(function (module) {
    var generateCaption = function(caption, cellsInRow) {
        return '<tr class="caption-row"><td class="caption-block" colspan="{0}">{1}</td></tr>'
            .format(cellsInRow, caption);
    };

    var generateWide = function(rowData, cellsInRow) {
        return '<tr class="wide-row"><td class="wide-block-wrapper" colspan="{0}"><div id="{1}"></div></td></tr>'
            .format(cellsInRow, rowData.id);
    };

    var generatePager = function(rowData, cellsInRow) {
        var content = '<div id="{0}-content"></div><div class="paginator" id="{1}-paginator"></div>'
            .format(rowData.id, rowData.id);

        return '<tr class="paginator-row"><td class="paginator-block-wrapper" colspan="{0}"><div id="{1}">{2}</div></td></tr>'
            .format(cellsInRow, rowData.id, content);
    };

    var generateCell = function(cell, cellsInRow) {
        var cellSize = 100 / cellsInRow;
        return ('<td class="cell-block" style="width: {0}%;">' +
            '<div class="cell-label">{1}</div>' +
            '<div class="cell-value" id="{2}"></div>' +
            '<div class="cell-additional">{3}</div>' +
            '</td>').format(cellSize, cell.label, cell.id, cell.additional);
    };

    var parseWides = function(rowsData, cellsInRow) {
        return rowsData.shiftWhile(function(row){
            return (row.type === 'wide');
        }).map(generateWide, cellsInRow).join('');
    };

    var parsePagers = function(rowsData, cellsInRow) {
        return rowsData.shiftWhile(function(row){
            return (row.type === 'pager');
        }).map(generatePager, cellsInRow).join('');
    };

    var parseCells = function(rowsData, cellsInRow) {
        var cells = rowsData.shiftWhile(function(row) {
            return (row.type === 'cell');
        }).map(generateCell, cellsInRow);

        var result = '';
        while (cells.length > 0) {
            var group = cells.shiftGroup(cellsInRow).map(function(e) {return e || '';});
            result += '<tr class="short-row">' + group.join('') + '</tr>';
        }

        return result;
    };

    var generateRows = function(rowsData, cellsInRow) {
        var result = '';
        while (rowsData.length > 0) {
            result += parsePagers(rowsData, cellsInRow);
            result += parseWides(rowsData, cellsInRow);
            result += parseCells(rowsData, cellsInRow);
        }

        return result;
    };

    var generateBlock = function(block) {
        var cellsInRow = block.cells || 3;

        var caption = generateCaption(block.caption, cellsInRow);
        var body = generateRows(block.rows, cellsInRow);

        var idPart = '';
        if (block.id) {
            idPart = 'id={0}'.format(block.id);
        }

        return '<table {0} class="details-block">{1}{2}</table>'.format(idPart, caption, body);
    };

    module.generate = function(blocks) {
        return blocks.map(generateBlock).join('');
    };

    module.update = function(data, arules) {
        var rules = arules || {};

        for (var id in data) {
            if (rules[id] !== undefined) {
                rules[id](id, data[id]);
            } else {
                $('#' + id).html(data[id]);
            }
        }
    };

    module.setupPager = function(id, itemsOnPage, listener) { 
        var onPageClick = function(pageNumber, event) {
            listener(pageNumber);
        };

        $("#{0}-paginator".format(id)).pagination({
            items: 1,
            itemsOnPage: itemsOnPage,
            cssStyle: 'light-theme',
            onPageClick: onPageClick
        });

        onPageClick(1, null);
    };

    module.updatePager = function(id, totalItems, content) { 
        $("#{0}-content".format(id)).html(content);
        $("#{0}-paginator".format(id)).pagination("updateItems", totalItems);
    };

    module.updateSpoiler = function(id, state) {
        var icon = $('#{0}-spoiler-icon'.format(id)); 
        var content = $('#{0}>tbody>tr:not(:first-child)'.format(id));

        if (state === undefined || state) {
            content.removeClass('hidden').addClass('visible');
            icon.removeClass('fa-angle-down').addClass('fa-angle-up');
        } else {
            content.removeClass('visible').addClass('hidden');
            icon.removeClass('fa-angle-up').addClass('fa-angle-down');
        }
    };

    module.setupSpoiler = function(id, state) {
        var head = $('#{0}>tbody>tr:first-child>td'.format(id));
        var newContent = '<i id="{0}-spoiler-icon" class="fa fa-angle-up"></i> {1}'.format(id, head.html());
        var link = '<a id="{0}-spoiler-link">{1}</a>'.format(id, newContent);
        head.html(link);

        module.updateSpoiler(id, state);

        $('#{0}-spoiler-link'.format(id)).on('click', function() {
            var content = $('#{0}>tbody>tr:not(:first-child)'.format(id));
            module.updateSpoiler(id, content.hasClass('hidden'));
        });
    };
})(grid);
