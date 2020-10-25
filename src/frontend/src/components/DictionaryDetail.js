import React, { useState } from 'react'
import { Tabs, Tab } from '@material-ui/core'

import Common from './common/Common'
import TokenList from './TokenList'
import TextList from './TextList'
import TagHelp from './TagHelp'

const TabPanel = ({value, index, children}) => (
  <div>{value === index && children}</div>
)

export default function(props) {
  const [value, setValue] = useState(0);
  const handleChange = (event, newValue) => {
    setValue(newValue);
  };
  console.log(props);
  return (
    <Common>
      <Tabs
	value={value}
	onChange={handleChange}
	indicatorColor="primary"
	textColor="primary"
	centered
      >
	<Tab label='Texts' />
	<Tab label='Words' />
    <Tab label='Tag help' />
      </Tabs>
      <TabPanel value={value} index={0}  >
          <TextList match={props.match}/>
      </TabPanel>
      <TabPanel value={value} index={1} >
          <TokenList match={props.match}/>
      </TabPanel>
      <TabPanel value={value} index={2} >
          <TagHelp />
      </TabPanel>
    </Common>
  )
}
