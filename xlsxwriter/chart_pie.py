###############################################################################
#
# ChartPie - A class for writing the Excel XLSX Pie charts.
#
# Copyright 2013-2014, John McNamara, jmcnamara@cpan.org
#

from warnings import warn
from . import chart


class ChartPie(chart.Chart):
    """
    A class for writing the Excel XLSX Pie charts.


    """

    ###########################################################################
    #
    # Public API.
    #
    ###########################################################################

    def __init__(self, options=None):
        """
        Constructor.

        """
        super(ChartPie, self).__init__()

        if options is None:
            options = {}

        self.vary_data_color = 1
        self.rotation = 0

        # Set the available data label positions for this chart type.
        self.label_position_default = 'best_fit'
        self.label_positions = {
            'center': 'ctr',
            'inside_end': 'inEnd',
            'outside_end': 'outEnd',
            'best_fit': 'bestFit'}

    def set_rotation(self, rotation):
        """
        Set the Pie/Doughnut chart rotation: the angle of the first slice.

        Args:
            rotation: First segment angle: 0 <= rotation <= 360.

        Returns:
            Nothing.

        """
        if rotation is None:
            return

        # Ensure the rotation is in Excel's range.
        if rotation < 0 or rotation > 360:
            warn("Chart rotation %d outside Excel range: 0 <= rotation <= 360"
                 % rotation)
            return

        self.rotation = int(rotation)

    ###########################################################################
    #
    # Private API.
    #
    ###########################################################################

    def _write_chart_type(self, args):
        # Override the virtual superclass method with a chart specific method.
        # Write the c:pieChart element.
        self._write_pie_chart(args)

    ###########################################################################
    #
    # XML methods.
    #
    ###########################################################################

    def _write_pie_chart(self, args):
        # Write the <c:pieChart> element.  Over-ridden method to remove
        # axis_id code since Pie charts don't require val and cat axes.
        self._xml_start_tag('c:pieChart')

        # Write the c:varyColors element.
        self._write_vary_colors()

        # Write the series elements.
        for data in self.series:
            self._write_ser(data)

        # Write the c:firstSliceAng element.
        self._write_first_slice_ang()

        self._xml_end_tag('c:pieChart')

    def _write_plot_area(self):
        # Over-ridden method to remove the cat_axis() and val_axis() code
        # since Pie charts don't require those axes.
        #
        # Write the <c:plotArea> element.

        self._xml_start_tag('c:plotArea')

        # Write the c:layout element.
        self._write_layout(self.plotarea.get('layout'), 'plot')

        # Write the subclass chart type element.
        self._write_chart_type(None)

        self._xml_end_tag('c:plotArea')

    def _write_legend(self):
        # Over-ridden method to add <c:txPr> to legend.
        # Write the <c:legend> element.

        position = self.legend_position
        font = self.legend_font
        delete_series = []
        overlay = 0

        if (self.legend_delete_series is not None
                and type(self.legend_delete_series) is list):
            delete_series = self.legend_delete_series

        if position.startswith('overlay_'):
            position = position.replace('overlay_', '')
            overlay = 1

        allowed = {
            'right': 'r',
            'left': 'l',
            'top': 't',
            'bottom': 'b',
        }

        if position == 'none':
            return

        if position not in allowed:
            return

        position = allowed[position]

        self._xml_start_tag('c:legend')

        # Write the c:legendPos element.
        self._write_legend_pos(position)

        # Remove series labels from the legend.
        for index in delete_series:
            # Write the c:legendEntry element.
            self._write_legend_entry(index)

        # Write the c:layout element.
        self._write_layout(self.legend_layout, 'legend')

        # Write the c:overlay element.
        if overlay:
            self._write_overlay()

        # Write the c:txPr element. Over-ridden.
        self._write_tx_pr_legend(None, font)

        self._xml_end_tag('c:legend')

    def _write_tx_pr_legend(self, horiz, font):
        # Write the <c:txPr> element for legends.

        if font and font.get('rotation'):
            rotation = font['rotation']
        else:
            rotation = None

        self._xml_start_tag('c:txPr')

        # Write the a:bodyPr element.
        self._write_a_body_pr(rotation, horiz)

        # Write the a:lstStyle element.
        self._write_a_lst_style()

        # Write the a:p element.
        self._write_a_p_legend(font)

        self._xml_end_tag('c:txPr')

    def _write_a_p_legend(self, font):
        # Write the <a:p> element for legends.

        self._xml_start_tag('a:p')

        # Write the a:pPr element.
        self._write_a_p_pr_legend(font)

        # Write the a:endParaRPr element.
        self._write_a_end_para_rpr()

        self._xml_end_tag('a:p')

    def _write_a_p_pr_legend(self, font):
        # Write the <a:pPr> element for legends.
        attributes = [('rtl', 0)]

        self._xml_start_tag('a:pPr', attributes)

        # Write the a:defRPr element.
        self._write_a_def_rpr(font)

        self._xml_end_tag('a:pPr')

    def _write_vary_colors(self):
        # Write the <c:varyColors> element.
        attributes = [('val', 1)]

        self._xml_empty_tag('c:varyColors', attributes)

    def _write_first_slice_ang(self):
        # Write the <c:firstSliceAng> element.
        attributes = [('val', self.rotation)]

        self._xml_empty_tag('c:firstSliceAng', attributes)
