import React from 'react';
import { Route, Switch, Router } from 'react-router';
import { Provider } from 'react-redux';
import store from './core/store';
import history from '../base/history';
import * as Pages from './components';
import { NotFoundPage } from '../components';
import { URLS } from '../config';
import Main from './Layout';

/* Antd styles */
import 'antd/lib/button/style/index.css';
import 'antd/lib/message/style/index.css';
import 'antd/lib/select/style/index.css';
import 'antd/lib/tabs/style/index.css';
import 'antd/lib/back-top/style/index.css';
import 'antd/lib/tooltip/style/index.css';
import 'antd/lib/layout/style/index.css';
import 'antd/lib/spin/style/index.css';
import 'antd/lib/row/style/css';
import 'antd/lib/col/style/css';

export default (
  <Provider store={store}>
    <Router history={history}>
      <Main>
        <Switch>
          <Route exact path={URLS.INDEX} component={Pages.IndexPage} />
          <Route exact path={URLS.VALIDATE} component={Pages.ValidatePage} />
          <Route exact path={URLS.RESULT} component={Pages.ResultPage} />
          <Route exact path={URLS.SAVED_TASK} component={Pages.SavedTaskPage} />
          <Route exact path={URLS.PROCESSING} component={Pages.ProcessingPage} />
          <Route path="*" component={NotFoundPage} />
        </Switch>
      </Main>
    </Router>
  </Provider>
);
