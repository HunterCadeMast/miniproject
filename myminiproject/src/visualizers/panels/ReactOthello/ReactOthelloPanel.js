/*globals define, _, WebGMEGlobal*/
/**
 * Generated by VisualizerGenerator 1.7.0 from webgme on Wed Dec 06 2023 15:11:40 GMT-0600 (Central Standard Time).
 */

define([
    'js/PanelBase/PanelBaseWithHeader',
    'js/PanelManager/IActivePanel',
    'widgets/ReactOthello/ReactOthelloWidget',
    './ReactOthelloControl'
], function (
    PanelBaseWithHeader,
    IActivePanel,
    ReactOthelloWidget,
    ReactOthelloControl
) {
    'use strict';

    function ReactOthelloPanel(layoutManager, params) {
        var options = {};
        //set properties from options
        options[PanelBaseWithHeader.OPTIONS.LOGGER_INSTANCE_NAME] = 'ReactOthelloPanel';
        options[PanelBaseWithHeader.OPTIONS.FLOATING_TITLE] = true;

        //call parent's constructor
        PanelBaseWithHeader.apply(this, [options, layoutManager]);

        this._client = params.client;
        this.appId = `ReactOthello-viz-id`;

        //initialize UI
        this._initialize();

        this.logger.debug('ctor finished');
    }

    //inherit from PanelBaseWithHeader
    _.extend(ReactOthelloPanel.prototype, PanelBaseWithHeader.prototype);
    _.extend(ReactOthelloPanel.prototype, IActivePanel.prototype);

    ReactOthelloPanel.prototype._initialize = function () {

        this.$el.prop('id', this.appId);
        this.$el.css({
            width: '100%',
            height: '100%',
        });

        this.control = new ReactOthelloControl({
            logger: this.logger,
            client: this._client
        });

        this.widget = null;

        this.onActivate();
    };

    ReactOthelloPanel.prototype.afterAppend = function afterAppend() {
        console.log('AFTER APPEND');
        /*if(!this.widget) {
            this.widget = ReactOthelloWidget(this.appId, this.control, this);
        }*/
        ReactOthelloWidget(this.appId, this.control);
    };

    /* OVERRIDE FROM WIDGET-WITH-HEADER */
    /* METHOD CALLED WHEN THE WIDGET'S READ-ONLY PROPERTY CHANGES */
    ReactOthelloPanel.prototype.onReadOnlyChanged = function (isReadOnly) {
        //apply parent's onReadOnlyChanged
        PanelBaseWithHeader.prototype.onReadOnlyChanged.call(this, isReadOnly);

    };

    /*ReactOthelloPanel.prototype.onResize = function (width, height) {
        this.logger.debug('onResize --> width: ' + width + ', height: ' + height);
        this.widget.onWidgetContainerResize(width, height);
    };*/

    /* * * * * * * * Visualizer life cycle callbacks * * * * * * * */
    ReactOthelloPanel.prototype.destroy = function () {
        this.control.destroy();
        // this.widget.destroy();

        PanelBaseWithHeader.prototype.destroy.call(this);
        WebGMEGlobal.KeyboardManager.setListener(undefined);
        WebGMEGlobal.Toolbar.refresh();
    };

    ReactOthelloPanel.prototype.onActivate = function () {
        // this.widget.onActivate();
        this.control.onActivate();
        WebGMEGlobal.KeyboardManager.setListener(this.widget);
        WebGMEGlobal.Toolbar.refresh();
    };

    ReactOthelloPanel.prototype.onDeactivate = function () {
        // this.widget.onDeactivate();
        this.control.onDeactivate();
        WebGMEGlobal.KeyboardManager.setListener(undefined);
        WebGMEGlobal.Toolbar.refresh();
    };

    return ReactOthelloPanel;
});
