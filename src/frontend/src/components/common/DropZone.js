import React from "react";
import Dropzone from 'react-dropzone';
import request from 'superagent';
import CloudUploadIcon from '@material-ui/icons/CloudUpload';
import IconButton from '@material-ui/core/IconButton';

const APP_API = process.env.APP_API || 'http://127.0.0.1:8000/api/';

class DropFiles extends React.Component {

  onDrop = (files, dictionaryId) => {
      var file = new FormData();
      file.append('file',files[0])
      var req=request
                .post(`${APP_API}dict/${dictionaryId}/texts/upload/`)
                .send(file);
      req.end(function(err,response){
          console.log("upload done!!!!!");
      });
    }

    render() {
        return (
           <Dropzone onDrop={(files) => {this.onDrop(files, this.props.dictionaryId)}}>
             {({getRootProps, getInputProps}) => (
               <section>
                 <div {...getRootProps()}>
                   <input {...getInputProps()} />
                       <IconButton
                            variant="contained"
                            color="default"
                            startIcon={<CloudUploadIcon />}
                          >
                        Upload
                      </IconButton>
                 </div>
               </section>
             )}
           </Dropzone>
        )
    }
}


export default DropFiles
