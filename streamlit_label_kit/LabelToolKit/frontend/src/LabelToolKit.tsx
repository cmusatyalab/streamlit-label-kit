import {
  withStreamlitConnection,
  ComponentProps
} from "streamlit-component-lib"
import { PythonArgs } from './utils'
import { Detection, Classification, Segmentation} from './label-tool'

const LabelToolKit = ({ args, theme }: ComponentProps) => {
  const {
    label_type,
  }: PythonArgs = args

  switch(label_type) {
    case "detection":
      return (Detection(args));
    case "annotation":
      return (Classification(args));
    case "segmentation":
      return (Segmentation(args));
    default:
      return null;
  }
}


export default withStreamlitConnection(LabelToolKit)