# Standard library imports
import sys
from functools  import cache
from time       import sleep
from webbrowser import open as open_browser
from subprocess import run as subprocess_run
from shutil     import rmtree as remove_directory
from timeit     import default_timer as timer

from typing    import Callable
from threading import Thread
from queue     import Empty, Full
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import ( 
    Process, 
    Queue          as multiprocessing_Queue,
    Event          as multiprocessing_Event,
    Pool           as multiprocessing_Pool,
    Manager        as multiprocessing_Manager,
    freeze_support as multiprocessing_freeze_support
)

from json import (
    load  as json_load, 
    dumps as json_dumps
)

from os import (
    sep       as os_separator,
    devnull   as os_devnull,
    getpid    as os_getpid,
    makedirs  as os_makedirs,
    listdir   as os_listdir,
    remove    as os_remove,
    fdopen    as os_fdopen,
    open      as os_open,
    rename    as os_rename,
    O_WRONLY,
    O_CREAT
)

from os.path import (
    basename   as os_path_basename,
    dirname    as os_path_dirname,
    abspath    as os_path_abspath,
    join       as os_path_join,
    exists     as os_path_exists,
    splitext   as os_path_splitext,
    expanduser as os_path_expanduser
)

from subprocess import (
    Popen as subprocess_Popen,
    STARTUPINFO,
    STARTF_USESHOWWINDOW
)

# Third-party library imports
from natsort import natsorted
from psutil import (
    Process             as psutil_Process,
    virtual_memory      as psutil_virtual_memory,
    IDLE_PRIORITY_CLASS as psutil_IDLE_PRIORITY_CLASS
)
from onnxruntime import (
    InferenceSession        as onnxruntime_InferenceSession,
    SessionOptions          as onnxruntime_SessionOptions,
    GraphOptimizationLevel  as onnxruntime_GraphOptimizationLevel,
    get_available_providers as onnxruntime_get_available_providers
)

from PIL.Image import (
    open      as pillow_image_open,
    fromarray as pillow_image_fromarray
)

from cv2 import (
    CAP_PROP_FPS,
    CAP_PROP_FRAME_COUNT,
    CAP_PROP_FRAME_HEIGHT,
    CAP_PROP_FRAME_WIDTH,
    COLOR_BGR2RGB,
    IMREAD_UNCHANGED,
    INTER_AREA,
    VideoCapture as opencv_VideoCapture,
    cvtColor     as opencv_cvtColor,
    imdecode     as opencv_imdecode,
    imencode     as opencv_imencode,
    cvtColor     as opencv_cvtColor,
    resize       as opencv_resize,
)

from numpy import (
    frombuffer  as numpy_frombuffer,
    concatenate as numpy_concatenate, 
    transpose   as numpy_transpose,
    expand_dims as numpy_expand_dims,
    squeeze     as numpy_squeeze,
    clip        as numpy_clip,
    mean        as numpy_mean,
    array_split as numpy_array_split,
    ndarray     as numpy_ndarray,
    float32,
    uint8
)

# GUI imports
from tkinter import (
    StringVar, 
    DISABLED
)
from customtkinter import (
    CTk,
    CTkFrame,
    CTkButton,
    CTkEntry,
    CTkFont,
    CTkImage,
    CTkLabel,
    CTkOptionMenu,
    CTkScrollableFrame,
    CTkToplevel,
    filedialog,
    set_appearance_mode,
    set_default_color_theme,
    set_widget_scaling,
    set_window_scaling
)

if sys.stdout is None: sys.stdout = open(os_devnull, "w")
if sys.stderr is None: sys.stderr = open(os_devnull, "w")

def find_by_relative_path(relative_path: str) -> str:
    base_path = getattr(sys, '_MEIPASS', os_path_dirname(os_path_abspath(__file__)))
    return os_path_join(base_path, relative_path)



app_name   = "FluidFrames"
version    = "2026.1"
githubme   = "https://github.com/Djdefrag/FluidFrames/releases"
telegramme = "https://linktr.ee/j3ngystudio"

app_name_color          = "#F08080"
background_color        = "#000000"
widget_background_color = "#181818"
text_color              = "#B8B8B8"


MENU_LIST_SEPARATOR     = [ "----" ]
AI_models_list          = [ "RIFE", "RIFE_s" ]
zoom_option_list        = [ "50%", "75%", "100%", "125%", "150%", "175%" ]
AI_multithreading_list  = [ "OFF", "2 threads", "4 threads", "6 threads", "8 threads"]
generation_options_list = [ "x2", "x4", "x8", "Slowmotion x2", "Slowmotion x4", "Slowmotion x8" ]
gpus_list               = [ "Auto", "GPU 1", "GPU 2", "GPU 3", "GPU 4" ]
keep_frames_list        = [ "ON", "OFF"]
image_extension_list    = [ ".jpg", ".png", ".bmp", ".tiff" ]
video_extension_list    = [ ".mp4", ".mkv", ".avi", ".mov" ]
video_codec_list   = [ 
    "x264",       "x265",       MENU_LIST_SEPARATOR[0],
    "h264_nvenc", "hevc_nvenc", MENU_LIST_SEPARATOR[0],
    "h264_amf",   "hevc_amf",   MENU_LIST_SEPARATOR[0],
    "h264_qsv",   "hevc_qsv",
    ]

OUTPUT_PATH_CODED    = "Same path as input files"
DOCUMENT_PATH        = os_path_join(os_path_expanduser('~'), 'Documents')
USER_PREFERENCE_PATH = find_by_relative_path(f"{DOCUMENT_PATH}{os_separator}{app_name}_{version}_UserPreference.json")
FFMPEG_EXE_PATH      = find_by_relative_path(f"Assets{os_separator}ffmpeg.exe")
EXIFTOOL_EXE_PATH    = find_by_relative_path(f"Assets{os_separator}exiftool.exe")

COMPLETED_STATUS = "Completed"
ERROR_STATUS     = "Error"
STOP_STATUS      = "Stop"
CLOSE_APP_STATUS = "CloseApp"


offset_y_options = 0.0825
row0  = 0.05
row1  = 0.125
row2  = row1 + offset_y_options
row3  = row2 + offset_y_options
row4  = row3 + offset_y_options
row5  = row4 + offset_y_options
row6  = row5 + offset_y_options
row7  = row6 + offset_y_options
row8  = row7 + offset_y_options
row9  = row8 + offset_y_options
row10 = row9 + offset_y_options

column_offset = 0.2
column_info1  = 0.625
column_info2  = 0.858
column_1      = 0.66
column_2      = column_1 + column_offset
column_1_5    = column_info1 + 0.08
column_1_4    = column_1_5 - 0.0127
column_3      = column_info2 + 0.08
column_2_9    = column_3 - 0.0127
column_3_5    = column_2 + 0.0355

little_textbox_width = 74
little_menu_width = 98

if sys.stdout is None: sys.stdout = open(os_devnull, "w")
if sys.stderr is None: sys.stderr = open(os_devnull, "w")

supported_file_extensions = [
    ".mp4", ".MP4", ".webm", ".WEBM", ".mkv", ".MKV",
    ".flv", ".FLV", ".gif", ".GIF", ".m4v", ".M4V",
    ".avi", ".AVI", ".mov", ".MOV", ".qt", ".3gp",
    ".mpg", ".mpeg", ".vob", ".VOB"
]

supported_video_extensions = [
    ".mp4", ".MP4", ".webm", ".WEBM", ".mkv", ".MKV",
    ".flv", ".FLV", ".gif", ".GIF", ".m4v", ".M4V",
    ".avi", ".AVI", ".mov", ".MOV", ".qt", ".3gp",
    ".mpg", ".mpeg", ".vob", ".VOB"
]



# AI -------------------

class AI_interpolation:

    # CLASS INIT FUNCTIONS

    def __init__(
            self, 
            AI_model_name:    str, 
            frame_gen_factor: int,
            directml_gpu:     str, 
            AI_input_height:  int,
            AI_input_width:   int
            ) -> None:
        
        # Passed variables
        self.AI_model_name    = AI_model_name
        self.frame_gen_factor = frame_gen_factor
        self.directml_gpu     = directml_gpu
        self.AI_input_height  = AI_input_height
        self.AI_input_width   = AI_input_width

        # Calculated variables
        self.AI_model_path = find_by_relative_path(f"AI-onnx{os_separator}{self.AI_model_name}_fp32.onnx")

        # Variable assigned later
        self.inferenceSession = None
        self.input_name       = None
        self.onnx_input       = None

    def _load_inferenceSession(self) -> onnxruntime_InferenceSession:

        providers = ['DmlExecutionProvider']

        match self.directml_gpu:
            case 'Auto':  provider_options = [{"performance_preference": "high_performance"}]
            case 'GPU 1': provider_options = [{"device_id": "0"}]
            case 'GPU 2': provider_options = [{"device_id": "1"}]
            case 'GPU 3': provider_options = [{"device_id": "2"}]
            case 'GPU 4': provider_options = [{"device_id": "3"}]

        sess_options                          = onnxruntime_SessionOptions()
        sess_options.enable_profiling         = False
        sess_options.graph_optimization_level = (onnxruntime_GraphOptimizationLevel.ORT_ENABLE_ALL)

        inference_session = onnxruntime_InferenceSession(
            path_or_bytes    = self.AI_model_path, 
            sess_options     = sess_options,
            providers        = providers,
            provider_options = provider_options,
        )

        return inference_session



    # INTERNAL CLASS FUNCTIONS

    def get_image_mode(self, image: numpy_ndarray) -> str:
        match image.shape:
            case (rows, cols):
                return "Grayscale"
            case (rows, cols, channels) if channels == 3:
                return "RGB"
            case (rows, cols, channels) if channels == 4:
                return "RGBA"

    def get_image_resolution(self, image: numpy_ndarray) -> tuple:
        height = image.shape[0]
        width  = image.shape[1]

        return height, width 

    def resize_with_AI_input_resolution(self, image: numpy_ndarray) -> numpy_ndarray:
        return opencv_resize(image, (self.AI_input_width, self.AI_input_height), interpolation = INTER_AREA)




    # AI CLASS FUNCTIONS

    def concatenate_images(self, image1: numpy_ndarray, image2: numpy_ndarray) -> numpy_ndarray:
        image1 = image1 / 255
        image2 = image2 / 255
        concateneted_image = numpy_concatenate((image1, image2), axis=2)
        return concateneted_image

    def preprocess_image(self, image: numpy_ndarray) -> numpy_ndarray:
        image = numpy_transpose(image, (2, 0, 1))
        image = numpy_expand_dims(image, axis=0)
        return image

    def onnxruntime_inference(self, image: numpy_ndarray) -> numpy_ndarray:
        self.onnx_input[self.input_name] = image
        onnx_output = self.inferenceSession.run(None, self.onnx_input)[0]

        return onnx_output

    def postprocess_output(self, onnx_output: numpy_ndarray) -> numpy_ndarray:
        onnx_output = numpy_squeeze(onnx_output, axis=0)
        onnx_output = numpy_clip(onnx_output, 0, 1)
        onnx_output = numpy_transpose(onnx_output, (1, 2, 0))

        return onnx_output.astype(float32)

    def de_normalize_image(self, onnx_output: numpy_ndarray, max_range: int) -> numpy_ndarray:    
        match max_range:
            case 255:   return (onnx_output * max_range).astype(uint8)
            case 65535: return (onnx_output * max_range).round().astype(float32)

    def AI_interpolation(self, image1: numpy_ndarray, image2: numpy_ndarray) -> numpy_ndarray:
        image        = self.concatenate_images(image1, image2).astype(float32)
        image        = self.preprocess_image(image)
        onnx_output  = self.onnxruntime_inference(image)
        onnx_output  = self.postprocess_output(onnx_output)     
        output_image = self.de_normalize_image(onnx_output, 255) 

        return output_image  



    # EXTERNAL FUNCTION

    def AI_orchestration(self, image1: numpy_ndarray, image2: numpy_ndarray) -> list[numpy_ndarray]:
        
        if self.inferenceSession == None:
            self.inferenceSession = self._load_inferenceSession()
            self.input_name       = self.inferenceSession.get_inputs()[0].name
            self.onnx_input       = { self.input_name: None }

        generated_images = []

        image1 = self.resize_with_AI_input_resolution(image1)
        image2 = self.resize_with_AI_input_resolution(image2)

        if self.frame_gen_factor == 2:   # Generate 1 image [image1 / image_A / image2]
            image_A = self.AI_interpolation(image1, image2)
            generated_images.append(image_A)

        elif self.frame_gen_factor == 4: # Generate 3 images [image1 / image_A / image_B / image_C / image2]
            image_B = self.AI_interpolation(image1, image2)
            image_A = self.AI_interpolation(image1, image_B)
            image_C = self.AI_interpolation(image_B, image2)

            generated_images.append(image_A)
            generated_images.append(image_B)
            generated_images.append(image_C)

        elif self.frame_gen_factor == 8: # Generate 7 images [image1 / image_A / image_B / image_C / image_D / image_E / image_F / image_G / image2]
            image_D = self.AI_interpolation(image1, image2)
            image_B = self.AI_interpolation(image1, image_D)
            image_A = self.AI_interpolation(image1, image_B)
            image_C = self.AI_interpolation(image_B, image_D)
            image_F = self.AI_interpolation(image_D, image2)
            image_E = self.AI_interpolation(image_D, image_F)
            image_G = self.AI_interpolation(image_F, image2)

            generated_images.append(image_A)
            generated_images.append(image_B)
            generated_images.append(image_C)
            generated_images.append(image_D)
            generated_images.append(image_E)
            generated_images.append(image_F)
            generated_images.append(image_G)

        return generated_images



# Frames sequence -------------------

class FrameSequence:

    def __init__(
            self, 
            start_frame_path:         str, 
            end_frame_path:           str,
            to_generate_frames_paths: list[str]
            ) -> None:

        self.start_frame_path              = start_frame_path
        self.end_frame_path                = end_frame_path
        self.to_generate_frames_paths      = to_generate_frames_paths
        self.frames_to_generate_number     = len(self.to_generate_frames_paths)
        self.is_sequence_already_generated = False


    # EXTERNAL FUNCTIONS

    def get_ordered_frame_path_list(self) -> list[str]:
        return [self.start_frame_path, *self.to_generate_frames_paths, self.end_frame_path]
    
    def check_if_sequence_already_generated(self) -> bool:
        if self.is_sequence_already_generated: return True
        
        if all(os_path_exists(path) for path in self.to_generate_frames_paths):
            self.is_sequence_already_generated = True
            return True
        
        return False

class FrameGenerationTask:

    def __init__(
            self, 
            video_path:            str, 
            video_output_path:     str,
            frame_gen_factor:      int,
            slowmotion:            bool,
            selected_video_codec:  str,
            input_resize_factor:   int,
            output_resize_factor:  int,
            frame_sequence_list:   list[FrameSequence],
            ) -> None:
        
        # Passed variables
        self.video_path           = video_path
        self.video_output_path    = video_output_path
        self.frame_gen_factor     = frame_gen_factor
        self.slowmotion           = slowmotion
        self.selected_video_codec = selected_video_codec
        self.input_resize_factor  = input_resize_factor
        self.output_resize_factor = output_resize_factor
        self.frame_sequence_list  = frame_sequence_list

        # Calculated variables
        self.effective_codec = self.selected_video_codec
        if   "x264" in self.selected_video_codec: self.effective_codec = "libx264"
        elif "x265" in self.selected_video_codec: self.effective_codec = "libx265"

        self.original_video_fps            = get_video_fps(self.video_path)
        self.target_video_fps              = self.original_video_fps if self.slowmotion else self.original_video_fps * self.frame_gen_factor
        self.frames_togenerate_total_count = self._get_frames_togenerate_total_count()
        
        self.AI_input_height = None
        self.AI_input_width  = None
        self.target_height   = None
        self.target_width    = None
        self._calculate_input_output_resolution()

        print(f"[FrameGenerationTask created]")
        print(f"   number of frame sequence: {len(self.frame_sequence_list)}")
        print(f"   number of frames to generate: {self.frames_togenerate_total_count}")
        print(f"   AI input resolution: {self.AI_input_width}x{self.AI_input_height}")
        print(f"   video output resolution: {self.target_width}x{self.target_height}")

    def _get_frames_togenerate_total_count(self) -> int:
        return sum(frame_sequence.frames_to_generate_number for frame_sequence in self.frame_sequence_list)

    def _get_image_resolution(self, image: numpy_ndarray) -> tuple:
        return image.shape[0], image.shape[1] 

    def _calculate_input_output_resolution(self) -> None:
        first_frame = image_read(self.frame_sequence_list[0].start_frame_path)
        
        original_height, original_width = self._get_image_resolution(first_frame)

        # AI input resolution
        self.AI_input_width  = int(original_width  * self.input_resize_factor)
        self.AI_input_height = int(original_height * self.input_resize_factor)

        self.AI_input_width  = self.AI_input_width if self.AI_input_width % 2 == 0 else self.AI_input_width + 1
        self.AI_input_height = self.AI_input_height if self.AI_input_height % 2 == 0 else self.AI_input_height + 1

        # Video output target resolution
        self.target_width  = int(original_width  * self.output_resize_factor)
        self.target_height = int(original_height * self.output_resize_factor)

        self.target_width  = self.target_width if self.target_width % 2 == 0 else self.target_width + 1
        self.target_height = self.target_height if self.target_height % 2 == 0 else self.target_height + 1


    # EXTERNAL FUNCTIONS

    def get_only_frame_sequence_to_generate(self) -> list[FrameSequence]:
        only_sequence_to_generate = []
        for sequence in self.frame_sequence_list:
            if not sequence.check_if_sequence_already_generated():
                only_sequence_to_generate.append(sequence)

        return only_sequence_to_generate

    def get_complete_frame_path_list(self) -> list[str]:
        complete_frame_path_list = []

        for frame_sequence in self.frame_sequence_list:
            complete_frame_path_list.extend(frame_sequence.get_ordered_frame_path_list())

        complete_frame_path_list = list(dict.fromkeys(complete_frame_path_list))

        return complete_frame_path_list
    
    def get_already_generated_frames_count(self) -> int:
        return sum(
            sum(1 for path in sequence.to_generate_frames_paths if os_path_exists(path))
            for sequence in self.frame_sequence_list
        )





# GUI utils ---------------------------

class MessageBox(CTkToplevel):

    def __init__(
            self,
            messageType: str,
            title: str,
            subtitle: str,
            default_value: str,
            option_list: list,
            ) -> None:

        super().__init__()

        self._running: bool = False

        self._messageType = messageType
        self._title       = title        
        self._subtitle    = subtitle
        self._default_value = default_value
        self._option_list   = option_list
        self._ctkwidgets_index = 0

        self.title('')
        self.lift()                          # lift window on top
        self.attributes("-topmost", True)    # stay on top
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.after(10, self._create_widgets)  # create widgets with slight delay, to avoid white flickering of background
        self.resizable(False, False)
        self.grab_set()                       # make other windows not clickable

    def _ok_event(
            self, 
            event = None
            ) -> None:
        self.grab_release()
        self.destroy()

    def _on_closing(
            self
            ) -> None:
        self.grab_release()
        self.destroy()

    def createEmptyLabel(self) -> CTkLabel:
        return CTkLabel(
            master   = self,
            fg_color = "transparent",
            width    = 500,
            height   = 17,
            text     = ''
        )

    def placeInfoMessageTitleSubtitle(self) -> None:

        spacingLabel1 = self.createEmptyLabel()
        spacingLabel2 = self.createEmptyLabel()

        if self._messageType == "info":
            title_subtitle_text_color = "#3399FF"
        elif self._messageType == "error":
            title_subtitle_text_color = "#FF3131"

        titleLabel = CTkLabel(
            master     = self,
            width      = 500,
            anchor     = 'w',
            justify    = "left",
            fg_color   = "transparent",
            text_color = title_subtitle_text_color,
            font       = bold22,
            text       = self._title
            )
        
        if self._default_value != None:
            defaultLabel = CTkLabel(
                master     = self,
                width      = 500,
                anchor     = 'w',
                justify    = "left",
                fg_color   = "transparent",
                text_color = "#3399FF",
                font       = bold17,
                text       = f"Default: {self._default_value}"
                )
        
        subtitleLabel = CTkLabel(
            master     = self,
            width      = 500,
            anchor     = 'w',
            justify    = "left",
            fg_color   = "transparent",
            text_color = title_subtitle_text_color,
            font       = bold14,
            text       = self._subtitle
            )
        
        spacingLabel1.grid(row = self._ctkwidgets_index, column = 0, columnspan = 2, padx = 0, pady = 0, sticky = "ew")
        
        self._ctkwidgets_index += 1
        titleLabel.grid(row = self._ctkwidgets_index, column = 0, columnspan = 2, padx = 25, pady = 0, sticky = "ew")
        
        if self._default_value != None:
            self._ctkwidgets_index += 1
            defaultLabel.grid(row = self._ctkwidgets_index, column = 0, columnspan = 2, padx = 25, pady = 0, sticky = "ew")
        
        self._ctkwidgets_index += 1
        subtitleLabel.grid(row = self._ctkwidgets_index, column = 0, columnspan = 2, padx = 25, pady = 0, sticky = "ew")
        
        self._ctkwidgets_index += 1
        spacingLabel2.grid(row = self._ctkwidgets_index, column = 0, columnspan = 2, padx = 0, pady = 0, sticky = "ew")

    def placeInfoMessageOptionsText(self) -> None:
        
        for option_text in self._option_list:
            optionLabel = CTkLabel(
                master        = self,
                width         = 600,
                height        = 45,
                anchor        = 'w',
                justify       = "left",
                text_color    = text_color,
                fg_color      = "#282828",
                bg_color      = "transparent",
                font          = bold13,
                text          = option_text,
                corner_radius = 10,
            )
            
            self._ctkwidgets_index += 1
            optionLabel.grid(row = self._ctkwidgets_index, column = 0, columnspan = 2, padx = 25, pady = 4, sticky = "ew")

        spacingLabel3 = self.createEmptyLabel()

        self._ctkwidgets_index += 1
        spacingLabel3.grid(row = self._ctkwidgets_index, column = 0, columnspan = 2, padx = 0, pady = 0, sticky = "ew")

    def placeInfoMessageOkButton(
            self
            ) -> None:
        
        ok_button = CTkButton(
            master  = self,
            command = self._ok_event,
            text    = 'OK',
            width   = 125,
            font         = bold11,
            border_width = 1,
            fg_color     = "#282828",
            text_color   = "#E0E0E0",
            border_color = "#0096FF"
        )
        
        self._ctkwidgets_index += 1
        ok_button.grid(row = self._ctkwidgets_index, column = 1, columnspan = 1, padx = (10, 20), pady = (10, 20), sticky = "e")

    def _create_widgets(
            self
            ) -> None:

        self.grid_columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        self.placeInfoMessageTitleSubtitle()
        self.placeInfoMessageOptionsText()
        self.placeInfoMessageOkButton()

class FileWidget(CTkScrollableFrame):

    def __init__(
            self, 
            master,
            selected_file_list, 
            frame_generation_factor = 1,
            input_resize_factor     = 0,
            output_resize_factor    = 0,
            **kwargs
            ) -> None:
        
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight = 1)

        self.file_list               = selected_file_list
        self.frame_generation_factor = frame_generation_factor
        self.input_resize_factor     = input_resize_factor
        self.output_resize_factor    = output_resize_factor

        self.index_row = 1
        self.ui_components = []
        self._create_widgets()

    def _destroy_(self) -> None:
        self.file_list = []
        self.destroy()
        place_loadFile_section()

    def _create_widgets(self) -> None:
        self.add_clean_button()
        for file_path in self.file_list:
            file_name_label, file_info_label = self.get_file_information(file_path)
            self.ui_components.append(file_name_label)
            self.ui_components.append(file_info_label)

    def get_file_information(self, file_path) -> tuple:
        infos, icon = self.extract_file_info(file_path)

        # File name
        file_name_label = CTkLabel(
            self, 
            text       = os_path_basename(file_path),
            font       = bold13,
            text_color = text_color,
            compound   = "left", 
            anchor     = "w",
            padx       = 10,
            pady       = 5,
            justify    = "left",
        )      
        file_name_label.grid(
            row    = self.index_row, 
            column = 0,
            pady   = (0, 2),
            padx   = (3, 3),
            sticky = "w"
        )

        # File infos and icon
        file_info_label = CTkLabel(
            self, 
            text       = infos,
            image      = icon, 
            font       = bold12,
            text_color = text_color,
            compound   = "left", 
            anchor     = "w",
            padx       = 10,
            pady       = 5,
            justify    = "left",
        )      
        file_info_label.grid(
            row    = self.index_row + 1, 
            column = 0,
            pady   = (0, 15),
            padx   = (3, 3),
            sticky = "w"
        )

        self.index_row += 2

        return file_name_label, file_info_label

    def add_clean_button(self) -> None:

        button = CTkButton(
            master        = self, 
            command       = self._destroy_,
            text          = "CLEAN",
            image         = clear_icon,
            width         = 90, 
            height        = 28,
            font          = bold11,
            border_width  = 1,
            corner_radius = 1,
            fg_color      = "#282828",
            text_color    = "#E0E0E0",
            border_color  = "#0096FF"
        )
        
        button.grid(row = 0, column=2, pady=(7, 7), padx = (0, 7))
        

    
    @cache
    def extract_file_icon(self, file_path) -> CTkImage:
        max_size = 60

        if check_if_file_is_video(file_path):
            video_cap   = opencv_VideoCapture(file_path)
            _, frame    = video_cap.read()
            source_icon = opencv_cvtColor(frame, COLOR_BGR2RGB)
            video_cap.release()
        else:
            source_icon = opencv_cvtColor(image_read(file_path), COLOR_BGR2RGB)

        ratio       = min(max_size / source_icon.shape[0], max_size / source_icon.shape[1])
        new_width   = int(source_icon.shape[1] * ratio)
        new_height  = int(source_icon.shape[0] * ratio)
        source_icon = opencv_resize(source_icon,(new_width, new_height))
        ctk_icon    = CTkImage(pillow_image_fromarray(source_icon, mode="RGB"), size = (new_width, new_height))

        return ctk_icon

    def extract_file_info(self, file_path) -> tuple:
        
        if check_if_file_is_video(file_path):
            cap          = opencv_VideoCapture(file_path)
            width        = round(cap.get(CAP_PROP_FRAME_WIDTH))
            height       = round(cap.get(CAP_PROP_FRAME_HEIGHT))
            num_frames   = int(cap.get(CAP_PROP_FRAME_COUNT))
            frame_rate   = cap.get(CAP_PROP_FPS)
            duration     = num_frames/frame_rate
            minutes      = int(duration/60)
            seconds      = duration % 60
            cap.release()

            file_icon  = self.extract_file_icon(file_path)
            file_infos = f"{minutes}m:{round(seconds)}s • {width}x{height} • {round(frame_rate, 2)} fps \n"
            
            if self.input_resize_factor != 0 and self.output_resize_factor != 0:
                input_resized_height = int(height * (self.input_resize_factor/100))
                input_resized_width  = int(width * (self.input_resize_factor/100))

                output_resized_height = int(height * (self.output_resize_factor/100))
                output_resized_width  = int(width * (self.output_resize_factor/100))

                if   "x2" in self.frame_generation_factor: generation_factor = 2
                elif "x4" in self.frame_generation_factor: generation_factor = 4
                elif "x8" in self.frame_generation_factor: generation_factor = 8

                if "Slowmotion" in self.frame_generation_factor: slowmotion = True
                else: slowmotion = False

                if slowmotion:
                    duration_slowmotion = (num_frames/frame_rate) * generation_factor
                    minutes_slowmotion  = int(duration_slowmotion/60)
                    seconds_slowmotion  = duration_slowmotion % 60

                    file_infos += (
                        f"AI input ({self.input_resize_factor}%) ➜ {input_resized_width}x{input_resized_height} • {round(frame_rate, 2)} fps \n"
                        f"AI output (x{generation_factor}-slow) ➜ {input_resized_width}x{input_resized_height} • {round(frame_rate, 2)} fps \n"
                        f"Video out. ({self.output_resize_factor}%) ➜ {minutes_slowmotion}m:{round(seconds_slowmotion)}s • {output_resized_width}x{output_resized_height} • {round(frame_rate, 2)} fps"
                    )
                    
                else:
                    fps_frame_generated = frame_rate * generation_factor

                    file_infos += (
                        f"AI input ({self.input_resize_factor}%) ➜ {input_resized_width}x{input_resized_height} • {round(frame_rate, 2)} fps \n"
                        f"AI output (x{generation_factor}) ➜ {input_resized_width}x{input_resized_height} • {round(fps_frame_generated, 2)} fps \n"
                        f"Video out. ({self.output_resize_factor}%) ➜ {output_resized_width}x{output_resized_height} • {round(fps_frame_generated, 2)} fps"
                    )


            return file_infos, file_icon



    # EXTERNAL FUNCTIONS

    def clean_file_list(self) -> None:
        self.index_row = 1
        for ui_component in self.ui_components: ui_component.grid_forget()

    def get_selected_file_list(self) -> list: 
        return self.file_list  

    def set_frame_generation_factor(self, frame_generation_factor) -> None:
        self.frame_generation_factor = frame_generation_factor

    def set_input_resize_factor(self, input_resize_factor) -> None:
        self.input_resize_factor = input_resize_factor

    def set_output_resize_factor(self, output_resize_factor) -> None:
        self.output_resize_factor = output_resize_factor
 


def get_values_for_file_widget() -> tuple:
    # Generation factor
    global selected_generation_option

    # Input resolution %
    try:
        input_resize_factor = int(float(str(selected_input_resize_factor.get())))
    except:
        input_resize_factor = 0

    # Output resolution %
    try:
        output_resize_factor = int(float(str(selected_output_resize_factor.get())))
    except:
        output_resize_factor = 0

    return selected_generation_option, input_resize_factor, output_resize_factor

def update_file_widget(a, b, c) -> None:
    try:
        global file_widget
        file_widget
    except:
        return
        
    generation_option, input_resize_factor, output_resize_factor = get_values_for_file_widget()

    file_widget.clean_file_list()
    file_widget.set_frame_generation_factor(generation_option)
    file_widget.set_input_resize_factor(input_resize_factor)
    file_widget.set_output_resize_factor(output_resize_factor)
    file_widget._create_widgets()

def create_option_background() -> CTkFrame:
    return CTkFrame(
        master   = window,
        bg_color = background_color,
        fg_color = widget_background_color,
        height   = 46,
        corner_radius = 10
    )

def create_info_button(
        command: Callable, 
        text:    str, 
        width:   int = 200
        ) -> CTkFrame:
    
    frame = CTkFrame(master = window, fg_color = widget_background_color, height = 25)

    button = CTkButton(
        master        = frame,
        command       = command,
        font          = bold12,
        text          = "?",
        border_color  = "#0096FF",
        border_width  = 1,
        fg_color      = widget_background_color,
        hover_color   = background_color,
        width         = 23,
        height        = 15,
        corner_radius = 1
    )
    button.grid(row=0, column=0, padx=(0, 7), pady=2, sticky="w")

    label = CTkLabel(
        master     = frame,
        text       = text,
        width      = width,
        height     = 22,
        fg_color   = "transparent",
        bg_color   = widget_background_color,
        text_color = text_color,
        font       = bold13,
        anchor     = "w"
    )
    label.grid(row=0, column=1, sticky="w")

    frame.grid_propagate(False)
    frame.grid_columnconfigure(1, weight=1)

    return frame

def create_option_menu(
        command:       Callable, 
        values:        list,
        default_value: str,
        border_color:  str = "#404040", 
        border_width:  int = 1,
        width:         int = 159,
        height:        int = 26
        ) -> CTkFrame:

    total_width  = (width + 2 * border_width)
    total_height = (height + 2 * border_width)
    
    frame = CTkFrame(
        master        = window,
        fg_color      = border_color,
        width         = total_width,
        height        = total_height,
        border_width  = 0,
        corner_radius = 1,
    )
    
    option_menu = CTkOptionMenu(
        master             = frame, 
        command            = command,
        values             = values,
        width              = width,
        height             = height,
        corner_radius      = 0,
        dropdown_font      = bold12,
        font               = bold11,
        anchor             = "center",
        text_color         = text_color,
        fg_color           = background_color,
        button_color       = background_color,
        button_hover_color = background_color,
        dropdown_fg_color  = background_color
    )
    
    option_menu.place(x = (total_width - width) / 2, y = (total_height - height) / 2)
    option_menu.set(default_value)
    return frame

def create_text_box(
        textvariable: StringVar, 
        width:        int,
        height:       int = 26
    ) -> CTkEntry:
    
    return CTkEntry(
        master        = window, 
        textvariable  = textvariable,
        corner_radius = 1,
        width         = width,
        height        = height,
        font          = bold11,
        justify       = "center",
        text_color    = text_color,
        fg_color      = "#000000",
        border_width  = 1,
        border_color  = "#404040",
    )

def create_text_box_output_path(
        textvariable: StringVar,
        height:       int = 26
    ) -> CTkEntry:
    
    return CTkEntry(
        master        = window, 
        textvariable  = textvariable,
        corner_radius = 1,
        width         = 250,
        height        = height,
        font          = bold11,
        justify       = "center",
        text_color    = text_color,
        fg_color      = "#000000",
        border_width  = 1,
        border_color  = "#404040",
        state         = DISABLED
    )

def create_active_button(
        command:      Callable,
        text:         str,
        icon:         CTkImage,
        width:        int = 140,
        height:       int = 30,
        border_color: str = "#0096FF"
    ) -> CTkButton:
    
    return CTkButton(
        master        = window, 
        command       = command,
        text          = text,
        image         = icon,
        width         = width,
        height        = height,
        font          = bold11,
        border_width  = 1,
        corner_radius = 1,
        fg_color      = "#282828",
        text_color    = "#E0E0E0",
        border_color  = border_color
    )

def create_link_button(
        command: Callable,
        icon:    CTkImage,
    ) -> CTkButton:

    return CTkButton(
        master        = window,
        command       = command,
        image         = icon,
        width         = 30,
        height        = 30,
        border_width  = 1,
        corner_radius = 1,
        fg_color      = "transparent",
        text_color    = text_color,
        border_color  = "#0096FF",
        anchor        = "center",
        text          = "", 
        font          = bold11
    )



# File Utils functions ------------------------

def image_read(file_path: str) -> numpy_ndarray: 
    with open(file_path, 'rb') as file:
        return opencv_imdecode(
            numpy_frombuffer(file.read(), uint8), 
            IMREAD_UNCHANGED
        )

def image_write(file_path: str, file_data: numpy_ndarray) -> None: 
    opencv_imencode(os_path_splitext(file_path)[1], file_data)[1].tofile(file_path)

def delete_file(file_path: str) -> None:
    if os_path_exists(file_path): os_remove(file_path)

def copy_file_metadata(original_file_path: str, target_file_path: str) -> None:
    
    exiftool_cmd = [
        EXIFTOOL_EXE_PATH, 
        '-fast', 
        '-TagsFromFile', 
        original_file_path, 
        '-overwrite_original', 
        '-all:all',
        '-unsafe',
        '-largetags', 
        target_file_path
    ]
    
    try: 
        subprocess_run(exiftool_cmd, check = True, shell = 'False')
    except:
        pass

def prepare_output_video_filename(
        video_path:               str, 
        selected_output_path:     str,
        selected_AI_model:        str,
        frame_gen_factor:         int, 
        slowmotion:               bool, 
        input_resize_factor:      int, 
        output_resize_factor:     int,
        selected_video_extension: str,
        ) -> str:
    

    if selected_output_path == OUTPUT_PATH_CODED:
        file_path_no_extension, _ = os_path_splitext(video_path)
        output_path = file_path_no_extension
    else:
        file_name = os_path_basename(video_path)
        file_path_no_extension, _ = os_path_splitext(file_name)
        output_path = f"{selected_output_path}{os_separator}{file_path_no_extension}"

    # Selected AI model
    to_append = f"_{selected_AI_model}x{str(frame_gen_factor)}"

    # Slowmotion?
    if slowmotion: to_append += f"_slowmo"

    # Selected input resize
    to_append += f"_InputR-{str(int(input_resize_factor * 100))}"

    # Selected output resize
    to_append += f"_OutputR-{str(int(output_resize_factor * 100))}"

    # Video output
    to_append += f"{selected_video_extension}"

    output_path += to_append

    return output_path

def prepare_output_video_directory_name(
        video_path:           str, 
        selected_output_path: str,
        selected_AI_model:    str,
        frame_gen_factor:     int, 
        slowmotion:           bool, 
        input_resize_factor:  int, 
        output_resize_factor: int 
        ) -> str:
    
    if selected_output_path == OUTPUT_PATH_CODED:
        file_path_no_extension, _ = os_path_splitext(video_path)
        output_path = file_path_no_extension
    else:
        file_name = os_path_basename(video_path)
        file_path_no_extension, _ = os_path_splitext(file_name)
        output_path = f"{selected_output_path}{os_separator}{file_path_no_extension}"

    # Selected AI model
    to_append = f"_{selected_AI_model}x{str(frame_gen_factor)}"

    # Slowmotion?
    if slowmotion: to_append += f"_slowmo"

    # Selected input resize
    to_append += f"_InputR-{str(int(input_resize_factor * 100))}"

    # Selected output resize
    to_append += f"_OutputR-{str(int(output_resize_factor * 100))}"

    output_path += to_append

    return output_path

def prepare_generated_frames_paths(
        base_path:                str,
        selected_AI_model:        str,
        selected_image_extension: str,
        frame_gen_factor:         int
        ) -> list[str]:
    
    generated_frames_paths = [f"{base_path}_{selected_AI_model}_{i}{selected_image_extension}" for i in range(frame_gen_factor-1)]
    
    return generated_frames_paths




# Image/video Utils functions ------------------------

def get_video_fps(video_path: str) -> float:
    video_capture = opencv_VideoCapture(video_path)
    frame_rate    = video_capture.get(CAP_PROP_FPS)
    video_capture.release()
    return frame_rate

def check_video_frame_generation_resume(
        target_directory:         str, 
        selected_AI_model:        str,
        selected_image_extension: str
        ) -> bool:
    
    if os_path_exists(target_directory):
        directory_files        = os_listdir(target_directory)
        generated_frames_paths = [file for file in directory_files if selected_AI_model in file]
        generated_frames_paths = [file for file in generated_frames_paths if file.endswith(selected_image_extension)]

        if len(generated_frames_paths) > 1:
            return True
        else:
            return False
    else:
        return False

def get_video_frames_for_frame_generation_resume(
        target_directory:         str,
        selected_AI_model:        str,
        selected_image_extension: str
        ) -> list[str]:
    
    # Only file names
    directory_files      = os_listdir(target_directory)
    original_frames_path = [file for file in directory_files if file.endswith(selected_image_extension)]
    original_frames_path = [file for file in original_frames_path if selected_AI_model not in file]

    # Adding the complete path to files
    original_frames_path = natsorted([os_path_join(target_directory, file) for file in original_frames_path])

    return original_frames_path

def calculate_time_to_complete_video(
        time_for_frame:   float, 
        remaining_frames: int
        ) -> str:
    
    remaining_time = time_for_frame * remaining_frames

    hours_left   = remaining_time // 3600
    minutes_left = (remaining_time % 3600) // 60
    seconds_left = round((remaining_time % 3600) % 60)

    time_left = ""

    if int(hours_left) > 0: 
        time_left = f"{int(hours_left):02d}h"
    
    if int(minutes_left) > 0: 
        time_left = f"{time_left}{int(minutes_left):02d}m"

    if seconds_left > 0: 
        time_left = f"{time_left}{seconds_left:02d}s"

    return time_left    

def check_frame_generation_option(selected_generation_option: str) -> tuple:
    slowmotion = False
    frame_gen_factor = 0

    if "Slowmotion" in selected_generation_option: slowmotion = True

    if   "2" in selected_generation_option: frame_gen_factor = 2
    elif "4" in selected_generation_option: frame_gen_factor = 4
    elif "8" in selected_generation_option: frame_gen_factor = 8

    return frame_gen_factor, slowmotion




# Core functions ------------------------

def check_frame_generation_steps() -> None:
    sleep(1)

    while True:
        actual_step = process_status_q.get()
        print(f"[{app_name}] check_frame_generation_steps - {actual_step}")

        if actual_step == CLOSE_APP_STATUS:
            break

        elif actual_step == STOP_STATUS:
            info_message.set(f"Frame generation stopped")
            place_generation_button()
            break

        elif actual_step == COMPLETED_STATUS:
            info_message.set(f"All files completed! :)")
            stop_framegeneration_process()
            place_generation_button()
            break

        elif ERROR_STATUS in actual_step:
            info_message.set(f"Error while generating :(")
            error_to_show = actual_step.replace(ERROR_STATUS, "")
            show_error_message(error_to_show.strip())
            stop_framegeneration_process()
            place_generation_button()
            break

        else:
            info_message.set(actual_step)

        sleep(1)

def write_process_status(
        process_status_q: multiprocessing_Queue, 
        step: str
        ) -> None:
    
    while not process_status_q.empty(): process_status_q.get()
    process_status_q.put(f"{step}")

def stop_framegeneration_process() -> None:
    global process_frame_generation_orchestrator

    print(f"[{app_name}] stop_framegeneration_process - framegeneration process stop event")
    event_stop_framegeneration_process.set()

    sleep(1)

    try:
        process_frame_generation_orchestrator
    except:
        pass
    else:
        print(f"[{app_name}] stop_framegeneration_process - waiting for framegeneration orchestrator to terminate")
        process_frame_generation_orchestrator.kill()
        print(f"[{app_name}] stop_framegeneration_process - framegeneration orchestrator terminated")
    
    try:
        while not process_status_q.empty(): process_status_q.get_nowait()
        print(f"[{app_name}] stop_framegeneration_process - process_status_q cleared")
    except Exception as e:
        print(f"[{app_name}] Warning clearing process_status_q: {e}")

    try:
        while not video_frames_and_info_q.empty(): video_frames_and_info_q.get_nowait()
        print(f"[{app_name}] stop_framegeneration_process - video_frames_and_info_q cleared")
    except Exception as e:
        print(f"[{app_name}] Warning clearing video_frames_and_info_q: {e}")

    event_stop_framegeneration_process.clear()

def stop_button_command() -> None:
    write_process_status(process_status_q, f"{STOP_STATUS}")
    stop_framegeneration_process()

# ORCHESTRATOR

def generate_button_command() -> None: 
    global selected_file_list
    global selected_AI_model
    global selected_generation_option
    global selected_AI_multithreading
    global selected_gpu
    global selected_image_extension
    global selected_video_extension
    global selected_keep_frames
    global selected_video_codec
    global input_resize_factor
    global output_resize_factor

    global process_frame_generation_orchestrator
    
    if user_input_checks():
        info_message.set("Loading")

        print("=" * 50)
        print(f"> Starting frame generation:")
        print(f"    Files to process: {len(selected_file_list)}")
        print(f"    Output path: {(selected_output_path.get())}")
        print(f"    Selected AI model: {selected_AI_model}")
        print(f"    Selected frame generation option: {selected_generation_option}")
        print(f"    AI multithreading: {selected_AI_multithreading}")
        print(f"    Selected image output extension: {selected_image_extension}")
        print(f"    Selected video output extension: {selected_video_extension}")
        print(f"    Selected video output codec: {selected_video_codec}")
        print(f"    Input resize factor: {int(input_resize_factor * 100)}%")
        print(f"    Output resize factor: {int(output_resize_factor * 100)}%")
        print(f"    Save frames: {selected_keep_frames}")
        print("=" * 50)

        place_stop_button()
        event_stop_framegeneration_process.clear()
        while not process_status_q.empty():        process_status_q.get_nowait()
        while not video_frames_and_info_q.empty(): video_frames_and_info_q.get_nowait()

        process_frame_generation_orchestrator = Process(
            target = frame_generation_orchestrator,
            args = (
                process_status_q, 
                video_frames_and_info_q,
                event_stop_framegeneration_process,
                selected_file_list, 
                selected_output_path.get(),
                selected_AI_model,
                selected_AI_multithreading,
                selected_generation_option, 
                input_resize_factor,
                output_resize_factor,
                selected_gpu,
                selected_keep_frames,
                selected_image_extension, 
                selected_video_extension, 
                selected_video_codec,
            )
        )
        process_frame_generation_orchestrator.start()

        Thread(target = check_frame_generation_steps).start()

def frame_generation_orchestrator(
        process_status_q:                   multiprocessing_Queue,
        video_frames_and_info_q:            multiprocessing_Queue,
        event_stop_framegeneration_process: multiprocessing_Event, # type: ignore

        selected_file_list:         list[str],
        selected_output_path:       str,
        selected_AI_model:          str,
        selected_AI_multithreading: int,
        selected_generation_option: str,
        input_resize_factor:        int,
        output_resize_factor:       int,
        selected_gpu:               str,
        selected_keep_frames:       bool,
        selected_image_extension:   str,
        selected_video_extension:   str,
        selected_video_codec:       str,
        ) -> None:
         
    frame_gen_factor, slowmotion = check_frame_generation_option(selected_generation_option)
    how_many_files = len(selected_file_list)

    try:
        for file_number in range(how_many_files):
            file_path   = selected_file_list[file_number]
            file_number = file_number + 1

            video_frame_generation(
                process_status_q                   = process_status_q,
                video_frames_and_info_q            = video_frames_and_info_q,
                event_stop_framegeneration_process = event_stop_framegeneration_process,
                video_path                         = file_path, 
                file_number                        = file_number,
                selected_output_path               = selected_output_path,
                selected_AI_model                  = selected_AI_model,
                frame_gen_factor                   = frame_gen_factor,
                selected_AI_multithreading         = selected_AI_multithreading, 
                selected_gpu                       = selected_gpu,
                slowmotion                         = slowmotion,
                input_resize_factor                = input_resize_factor,
                output_resize_factor               = output_resize_factor,
                selected_keep_frames               = selected_keep_frames,
                selected_image_extension           = selected_image_extension, 
                selected_video_extension           = selected_video_extension,
                selected_video_codec               = selected_video_codec,
            )

        write_process_status(process_status_q, f"{COMPLETED_STATUS}")

    except Exception as exception:
        write_process_status(process_status_q, f"{ERROR_STATUS} {str(exception)}")



# FRAME GENERATION

def generate_video_frames_async(
        video_frames_and_info_q:            multiprocessing_Queue,
        event_stop_framegeneration_process: multiprocessing_Event, # type: ignore
        frame_sequence_chunks:              list[FrameSequence],
        frame_generation_task:              FrameGenerationTask,
        selected_AI_model:                  str,
        selected_AI_multithreading:         int,
        selected_gpu:                       str,
        ) -> None:
        
    process_pid = os_getpid()
    psutil_Process(process_pid).nice(psutil_IDLE_PRIORITY_CLASS)

    AI_instance = AI_interpolation(
        selected_AI_model, 
        frame_generation_task.frame_gen_factor, 
        selected_gpu, 
        frame_generation_task.AI_input_height, 
        frame_generation_task.AI_input_width
    )
    
    for frame_sequence in frame_sequence_chunks:
        
        start_timer = timer()

        if event_stop_framegeneration_process.is_set():
            print("[Frame generation process] Terminating early due to stop event")
            break

        # Read frames
        frame_1 = image_read(frame_sequence.start_frame_path)
        frame_2 = image_read(frame_sequence.end_frame_path)
        
        # Generate frames
        generated_frames = AI_instance.AI_orchestration(frame_1, frame_2)

        # Calculate processing time
        end_timer       = timer()
        processing_time = round((end_timer - start_timer)/selected_AI_multithreading, 3)
        
        # Add things in queue
        success = False
        while success == False:
            try:
                video_frames_and_info_q.put_nowait(
                    {
                        "generated_frames_paths": frame_sequence.to_generate_frames_paths,
                        "generated_frames":       generated_frames,
                        "processing_time":        processing_time
                    }
                )
                success = True
                break
            except Full:
                sleep(0.1)

    if event_stop_framegeneration_process.is_set():
        print(f"[Frame-generation process {process_pid}] Terminated")
    else:
        print(f"[Frame-generation process {process_pid}] finished the job")

def video_frame_generation(
        process_status_q:                   multiprocessing_Queue,
        video_frames_and_info_q:            multiprocessing_Queue,
        event_stop_framegeneration_process: multiprocessing_Event, # type: ignore

        video_path:                 str, 
        file_number:                int,
        selected_output_path:       str,
        selected_AI_model:          str,
        frame_gen_factor:           int, 
        selected_AI_multithreading: int,
        selected_gpu:               str,
        slowmotion:                 bool, 
        input_resize_factor:        int,
        output_resize_factor:       int,
        selected_keep_frames:       bool,
        selected_image_extension:   str,
        selected_video_extension:   str,
        selected_video_codec:       str,
        ) -> None:
    
    
    # Internal functions

    def create_dir(name_dir: str) -> None:
        
        if os_path_exists(name_dir):     remove_directory(name_dir)
        if not os_path_exists(name_dir): os_makedirs(name_dir, mode=0o777)

        if sys.platform == "win32":
            try:
                subprocess_run(
                    ["attrib", "+I", "/S", "/D", name_dir],
                    check = False,
                    shell = True
                )
            except Exception as e:
                print(f"[create_dir] Error setting +I attribute: {e}")

            try:
                desktop_ini = os_path_join(name_dir, "desktop.ini")
                with open(desktop_ini, "w", encoding="utf-8") as f: f.write("[.ShellClassInfo]\nNoIndexing=1\n")
            except Exception as e:
                print(f"[create_dir] Error creating desktop.ini: {e}")

            try:
                subprocess_run(
                    ["attrib", "+S", name_dir],
                    check = False,
                    shell = True
                )
            except Exception as e:
                print(f"[create_dir] Error setting +S attribute on folder: {e}")

            try:
                subprocess_run(
                    ["attrib", "+H", desktop_ini],
                    check = False,
                    shell = True
                )
            except Exception as e:
                print(f"[create_dir] Error setting +H attribute on desktop.ini: {e}")

    def monitor_extraction_progress(
            process_status_q:      multiprocessing_Queue,
            stop_extraction_event: multiprocessing_Event, # type: ignore
            file_number:           int,
            target_directory:      str,
            total_video_frames:    int,
            ) -> None:

        while not stop_extraction_event.is_set():
            sleep(3)
            extracted_frames_number = len(
                [
                    f for f in os_listdir(target_directory)
                    if f.startswith("frame_")
                ]
            )
            percent_complete = int((extracted_frames_number / total_video_frames) * 100 if total_video_frames > 0 else 0)
            write_process_status(process_status_q, f"{file_number}. Extracting video frames {percent_complete}%")

    def prepare_frame_sequence_list(
            extracted_frames_paths:   list[str],
            selected_AI_model:        str,
            frame_gen_factor:         int,
            selected_image_extension: str
            ) -> list[FrameSequence]:

        frame_sequence_list: list[FrameSequence] = []

        for index in range(len(extracted_frames_paths)-1):
            start_frame_path         = extracted_frames_paths[index]
            end_frame_path           = extracted_frames_paths[index+1]
            base_path                = os_path_splitext(start_frame_path)[0]
            to_generate_frames_paths = prepare_generated_frames_paths(base_path, selected_AI_model, selected_image_extension, frame_gen_factor)

            frame_sequence_list.append(FrameSequence(start_frame_path, end_frame_path, to_generate_frames_paths))

        return frame_sequence_list

    def extract_video_frames(
            process_status_q:                   multiprocessing_Queue,
            event_stop_framegeneration_process: multiprocessing_Event, # type: ignore
            file_number:                        int,
            target_directory:                   str,
            video_path:                         str,
            selected_image_extension:           str
            ) -> list[str]:

        # 1. Get total number of frames and fps
        video_capture       = opencv_VideoCapture(video_path)
        video_frames_number = int(video_capture.get(CAP_PROP_FRAME_COUNT))
        video_fps           = video_capture.get(CAP_PROP_FPS)
        video_capture.release()

        # 2. Create directory to extract frames
        create_dir(target_directory)

        # 3. Start monitoring thread
        stop_extraction_event = multiprocessing_Event()
        monitor_thread = Thread(
            target = monitor_extraction_progress,
            args = (
                process_status_q,
                stop_extraction_event,
                file_number,
                target_directory,
                video_frames_number
            ),
            daemon = True
        )
        monitor_thread.start()

        # 4. Create FFMPEG command to extract video frames
        output_pattern = os_path_join(target_directory, f"frame_%03d{selected_image_extension}")
        extraction_command = [
            FFMPEG_EXE_PATH,
            "-y",
            "-loglevel",   "error",
            "-err_detect", "ignore_err",
            "-i",          video_path,
            "-vf",         f"fps={video_fps}",
            "-qscale:v",   "1",
            output_pattern
        ]
        
        # 5. Execute FFMPEG command
        startupinfo = None
        if sys.platform == "win32":
            startupinfo = STARTUPINFO()
            startupinfo.dwFlags |= STARTF_USESHOWWINDOW

        ffmpeg_process = None
        try:
            ffmpeg_process = subprocess_Popen(extraction_command, startupinfo = startupinfo)
            try: psutil_Process(ffmpeg_process.pid).nice(psutil_IDLE_PRIORITY_CLASS)
            except Exception: pass
            while ffmpeg_process.poll() is None:
                if event_stop_framegeneration_process.is_set():
                    print("[FFMPEG] Terminating early due to stop event")
                    ffmpeg_process.terminate()
                    ffmpeg_process.wait()
                    stop_extraction_event.set()
                    monitor_thread.join()
                    return []
                sleep(0.1)

        except Exception as e:
            write_process_status(process_status_q, f"{ERROR_STATUS} Frame extraction failed: {e}")
            if ffmpeg_process: ffmpeg_process.kill()
            stop_extraction_event.set()
            monitor_thread.join()
            return []

        # 6. Stop monitoring thread
        stop_extraction_event.set()
        monitor_thread.join()

        # 7. Get extracted frames paths and return
        extracted_files = [
            os_path_join(target_directory, f)
            for f in natsorted(os_listdir(target_directory))
            if f.endswith(f"{selected_image_extension}") and f.startswith("frame_")
        ]

        return extracted_files

    def video_encoding(
            process_status_q:      multiprocessing_Queue,
            frame_generation_task: FrameGenerationTask
            ) -> None:

        video_path               = str(frame_generation_task.video_path)
        video_output_path        = str(frame_generation_task.video_output_path)
        slowmotion               = frame_generation_task.slowmotion
        complete_frame_path_list = frame_generation_task.get_complete_frame_path_list()
        effective_codec          = str(frame_generation_task.effective_codec)
        target_video_fps         = str(frame_generation_task.target_video_fps)
        target_video_width       = str(frame_generation_task.target_width)
        target_video_height      = str(frame_generation_task.target_height)

        output_video_txt_path   = f"{os_path_splitext(video_output_path)[0]}.txt"
        blank_output_video_path = f"{os_path_splitext(video_output_path)[0]}_no_audio{os_path_splitext(video_output_path)[1]}"

        # Cleaning files from previous encoding
        delete_file(blank_output_video_path)
        delete_file(output_video_txt_path)

        # Create a file .txt with all video frames paths (original+generated) || this file is essential
        with os_fdopen(os_open(output_video_txt_path, O_WRONLY | O_CREAT, 0o777), 'w', encoding = "utf-8") as txt:
            for frame_path in complete_frame_path_list:
                if os_path_exists(frame_path):
                    txt.write(f"file '{frame_path}' \n")

        # Create the final video without audio
        print(f"[FFMPEG] ENCODING ({effective_codec})")
        try: 
            encoding_command = [
                FFMPEG_EXE_PATH,
                "-y",
                "-loglevel",    "error",
                "-f",           "concat",
                "-safe",        "0",
                "-r",           target_video_fps,
                "-i",           output_video_txt_path,
                "-c:v",         effective_codec,
                "-g",           target_video_fps,
                "-vf",          f"scale={target_video_width}:{target_video_height},format=yuv420p",
                "-color_range", "tv",
                "-movflags",    "+faststart",
                "-b:v",         "20000k",
                blank_output_video_path
            ]
            subprocess_run(encoding_command, check = True, shell = "False")
            delete_file(output_video_txt_path)
        except:
            write_process_status(
                process_status_q, 
                f"{ERROR_STATUS}An error occurred during video encoding. \n Have you selected a codec compatible with your GPU? If the issue persists, try selecting 'x264'."
            )

        if slowmotion: # Skip audio passthrough and rename the video without audio
            os_rename(blank_output_video_path, video_output_path)
        else:
            # Copy the audio from original video
            print("[FFMPEG] AUDIO PASSTHROUGH")
            audio_passthrough_command = [
                FFMPEG_EXE_PATH,
                "-y",
                "-loglevel", "error",
                "-i",        video_path,
                "-i",        blank_output_video_path,
                "-c:v",      "copy",
                "-map",      "1:v:0",
                "-map",      "0:a?",
                "-c:a",      "copy",
                video_output_path
            ]
            try: 
                subprocess_run(audio_passthrough_command, check = True, shell = "False")
                delete_file(blank_output_video_path)
            except:
                pass

    def update_video_process_status(
            process_status_q:         multiprocessing_Queue, 
            file_number:              int, 
            frame_generation_task:    FrameGenerationTask,
            average_processing_time:  float
            ) -> None:
        
        frames_togenerate_total_count  = frame_generation_task.frames_togenerate_total_count
        already_generated_frames_count = frame_generation_task.get_already_generated_frames_count()

        # Generated frames  
        remaining_frames = frames_togenerate_total_count - already_generated_frames_count
        remaining_time   = calculate_time_to_complete_video(average_processing_time, remaining_frames)
        if remaining_time != "":
            percent_complete = int((already_generated_frames_count / frames_togenerate_total_count) * 100)
            write_process_status(process_status_q, f"{file_number}. Video frame generation {percent_complete}% ({remaining_time})")

    def manage_video_frames_save_on_disk(
            process_status_q:                       multiprocessing_Queue,
            video_frames_and_info_q:                multiprocessing_Queue,
            event_stop_framegeneration_process:     multiprocessing_Event, # type: ignore
            event_stop_framegeneration_save_thread: multiprocessing_Event, # type: ignore
            file_number:                            int,
            frame_generation_task:                  FrameGenerationTask,
            ) -> None:
            
        def _internal_save_frames(frame_path_list: list[str], frame_list: list[numpy_ndarray]) -> None:
            for index, _ in enumerate(frame_path_list): 
                frame_path = frame_path_list[index]
                frame      = frame_list[index]
                image_write(
                    file_path = frame_path, 
                    file_data = frame
                )
        
        
        # Main
        processing_times_list   = []

        UPDATE_STATUS_TIMER     = 3.0
        MAX_UPDATE_STATUS_TIMER = 10.0
        MIN_UPDATE_STATUS_TIMER = 3.0
        TIMER_TICK_PLUS         = 1.5
        TIMER_TICK_MINUS        = 0.5
        can_you_change_timer    = False
        last_update_time        = timer()

        with ThreadPoolExecutor(max_workers=4) as executor:
            threads_set = set()

            while True:
                if event_stop_framegeneration_process.is_set():
                    print(f"[Video frames save thread] terminating by framegeneration stop event")
                    break

                if event_stop_framegeneration_save_thread.is_set() and video_frames_and_info_q.empty():
                    print(f"[Video frames save thread] terminating correctly")
                    break

                # 1. If the video frames queue is full we extend UPDATE_STATUS_TIMER
                if video_frames_and_info_q.full() and can_you_change_timer:
                    can_you_change_timer = False
                    UPDATE_STATUS_TIMER += TIMER_TICK_PLUS
                    if UPDATE_STATUS_TIMER > MAX_UPDATE_STATUS_TIMER: UPDATE_STATUS_TIMER = MAX_UPDATE_STATUS_TIMER

                # 2. If the video frames queue has < 25 elements we remove time from UPDATE_STATUS_TIMER
                if video_frames_and_info_q.qsize() < 25 and can_you_change_timer:
                    can_you_change_timer = False
                    UPDATE_STATUS_TIMER -= TIMER_TICK_MINUS
                    if UPDATE_STATUS_TIMER < MIN_UPDATE_STATUS_TIMER: UPDATE_STATUS_TIMER = MIN_UPDATE_STATUS_TIMER

                # 3. Read frames, paths and processing time from queue
                try:
                    item = video_frames_and_info_q.get_nowait()
                except Empty:
                    sleep(0.1)
                    continue

                generated_frames_paths = item["generated_frames_paths"]
                generated_frames       = item["generated_frames"]
                processing_time        = item["processing_time"]

                # 4. Resize with output factor and save frams
                threads_set.add(
                    executor.submit(
                        _internal_save_frames, 
                        generated_frames_paths, 
                        generated_frames
                    )
                )

                processing_times_list.append(processing_time)
                now = timer()
                if now - last_update_time >= UPDATE_STATUS_TIMER:
                    # 5. Update timer
                    can_you_change_timer = True
                    last_update_time     = now

                    # 6. Clean threads_set removing completed threads
                    done_threads = {t for t in threads_set if t.done()}
                    threads_set -= done_threads
                        
                    # 7. Calculate the % completion and ETA
                    if processing_times_list:
                        update_video_process_status(
                            process_status_q        = process_status_q,
                            file_number             = file_number, 
                            frame_generation_task   = frame_generation_task, 
                            average_processing_time = numpy_mean(processing_times_list)
                        )
                        processing_times_list = []
                        
            for t in threads_set: t.result()
   
    def generate_video_frames(
            process_status_q:                   multiprocessing_Queue,
            video_frames_and_info_q:            multiprocessing_Queue,
            event_stop_framegeneration_process: multiprocessing_Event, # type: ignore
            file_number:                        int,
            frame_generation_task:              FrameGenerationTask,
            selected_AI_model:                  str,
            selected_AI_multithreading:         int, 
            selected_gpu:                       str,
            ) -> None:
        
        event_stop_framegeneration_save_thread = multiprocessing_Event()
        Thread(
            target = manage_video_frames_save_on_disk,
            args   = (
                process_status_q, 
                video_frames_and_info_q,
                event_stop_framegeneration_process,
                event_stop_framegeneration_save_thread,
                file_number,
                frame_generation_task,
            )
        ).start()

        frame_sequence_chunks = numpy_array_split(
            frame_generation_task.get_only_frame_sequence_to_generate(), 
            selected_AI_multithreading
        )
        frame_sequence_chunks = [list(chunk) for chunk in frame_sequence_chunks]

        with multiprocessing_Pool(selected_AI_multithreading) as pool:
            pool.starmap(
                generate_video_frames_async,
                zip(
                    repeat(video_frames_and_info_q),
                    repeat(event_stop_framegeneration_process),
                    frame_sequence_chunks,
                    repeat(frame_generation_task),
                    repeat(selected_AI_model),
                    repeat(selected_AI_multithreading),
                    repeat(selected_gpu)
                )
            )
    
        write_process_status(process_status_q, f"{file_number}. Finalizing frame generation")
        event_stop_framegeneration_save_thread.set()
        sleep(5)


    # Main function
    
    # 1. Resume frame generation OR extract video frames
    target_directory        = prepare_output_video_directory_name(video_path, selected_output_path, selected_AI_model, frame_gen_factor, slowmotion,  input_resize_factor, output_resize_factor)
    frame_generation_resume = check_video_frame_generation_resume(target_directory, selected_AI_model, selected_image_extension)
    
    if frame_generation_resume:
        write_process_status(process_status_q, f"{file_number}. Resume frame generation")
        extracted_frames_paths = get_video_frames_for_frame_generation_resume(
            target_directory         = target_directory,
            selected_AI_model        = selected_AI_model, 
            selected_image_extension = selected_image_extension
        )
    else:
        write_process_status(process_status_q, f"{file_number}. Extracting video frames")
        extracted_frames_paths = extract_video_frames(
            process_status_q                   = process_status_q,
            event_stop_framegeneration_process = event_stop_framegeneration_process,
            file_number                        = file_number, 
            target_directory                   = target_directory, 
            video_path                         = video_path,
            selected_image_extension           = selected_image_extension
        )


    # 2. Create FrameGenerationTask with all informations about this Task
    frame_generation_task = FrameGenerationTask(
        video_path           = video_path,
        video_output_path    = prepare_output_video_filename(video_path, selected_output_path, selected_AI_model, frame_gen_factor, slowmotion, input_resize_factor, output_resize_factor, selected_video_extension),
        frame_gen_factor     = frame_gen_factor,
        slowmotion           = slowmotion,
        selected_video_codec = selected_video_codec,
        input_resize_factor  = input_resize_factor,
        output_resize_factor = output_resize_factor,
        frame_sequence_list  = prepare_frame_sequence_list(extracted_frames_paths, selected_AI_model, frame_gen_factor, selected_image_extension),
    )


    # 3. Frame generation
    write_process_status(process_status_q, f"{file_number}. Video frame generation")
    generate_video_frames(
        process_status_q                   = process_status_q,
        video_frames_and_info_q            = video_frames_and_info_q,
        event_stop_framegeneration_process = event_stop_framegeneration_process,
        file_number                        = file_number,
        frame_generation_task              = frame_generation_task,
        selected_AI_model                  = selected_AI_model, 
        selected_gpu                       = selected_gpu,
        selected_AI_multithreading         = selected_AI_multithreading,
    )


    # 4. Video encoding
    write_process_status(process_status_q, f"{file_number}. Encoding frame-generated video")
    video_encoding(process_status_q, frame_generation_task)
    copy_file_metadata(
        original_file_path = frame_generation_task.video_path, 
        target_file_path   = frame_generation_task.video_output_path
    )


    # 5. Delete frames folder
    if selected_keep_frames == False: 
        if os_path_exists(target_directory): 
            remove_directory(target_directory)




# GUI function ---------------------------

def apply_app_zoom(zoom: float) -> None:
    set_window_scaling(zoom)
    set_widget_scaling(zoom)

def user_input_checks() -> None:
    global selected_file_list
    global selected_generation_option
    global selected_image_extension
    global input_resize_factor
    global output_resize_factor

    is_ready = True

    # Selected files 
    try: selected_file_list = file_widget.get_selected_file_list()
    except:
        info_message.set("No file selected. Please select a file")
        is_ready = False

    if len(selected_file_list) <= 0:
        info_message.set("No file selected. Please select a file")
        is_ready = False

    # Input resize factor 
    try: input_resize_factor = int(float(str(selected_input_resize_factor.get())))
    except:
        info_message.set("Input resolution % must be a number")
        return False

    if input_resize_factor > 0: input_resize_factor = input_resize_factor/100
    else:
        info_message.set("Input resolution % must be a value > 0")
        return False


    # Output resize factor 
    try: output_resize_factor = int(float(str(selected_output_resize_factor.get())))
    except:
        info_message.set("Output resolution % must be a number")
        return False

    if output_resize_factor > 0: output_resize_factor = output_resize_factor/100
    else:
        info_message.set("Output resolution % must be a value > 0")
        return False

    return is_ready

def check_if_file_is_video(file: str) -> bool:
    return any(video_extension in file for video_extension in supported_video_extensions)

def check_supported_selected_files(uploaded_file_list: list) -> list:
    return [file for file in uploaded_file_list if any(supported_extension in file for supported_extension in supported_file_extensions)]

def show_error_message(exception: str) -> None:
    messageBox_title    = "Frame generation error"
    messageBox_subtitle = "Please report the error on Github or Telegram"
    messageBox_text     = f"\n {str(exception)} \n"

    MessageBox(
        messageType   = "error",
        title         = messageBox_title,
        subtitle      = messageBox_subtitle,
        default_value = None,
        option_list   = [messageBox_text]
    )

def open_files_action() -> None:
    info_message.set("Selecting files")

    uploaded_files_list    = list(filedialog.askopenfilenames())
    uploaded_files_counter = len(uploaded_files_list)

    supported_files_list    = check_supported_selected_files(uploaded_files_list)
    supported_files_counter = len(supported_files_list)
    
    print("> Uploaded files: " + str(uploaded_files_counter) + " => Supported files: " + str(supported_files_counter))

    if supported_files_counter > 0:
        global file_widget

        generation_option, input_resize_factor, output_resize_factor = get_values_for_file_widget()

        file_widget = FileWidget(
            master                  = window, 
            selected_file_list      = supported_files_list,
            frame_generation_factor = generation_option,
            input_resize_factor     = input_resize_factor,
            output_resize_factor    = output_resize_factor,
            fg_color                = background_color, 
            bg_color                = background_color
        )
        file_widget.place(relx = 0.0, rely = 0.0, relwidth = 0.5, relheight = 1.0)
        info_message.set("Ready")

    else: 
        info_message.set("Not supported files :(")

def open_output_path_action() -> None:
    asked_selected_output_path = filedialog.askdirectory()
    if asked_selected_output_path == "":
        selected_output_path.set(OUTPUT_PATH_CODED)
    else:
        selected_output_path.set(asked_selected_output_path)




# GUI select from menus functions ---------------------------

def select_app_zoom(selected_option: str) -> None:
    global selected_app_zoom
    selected_app_zoom = selected_option
    apply_app_zoom(float(selected_option.replace("%", "")) / 100)

def select_AI_from_menu(selected_option: str) -> None:
    global selected_AI_model    
    selected_AI_model = selected_option

def select_framegeneration_option_from_menu(selected_option: str):
    global selected_generation_option    
    selected_generation_option = selected_option
    update_file_widget(1,2,3)

def select_AI_multithreading_from_menu(selected_option: str) -> None:
    global selected_AI_multithreading
    if selected_option == "OFF": 
        selected_AI_multithreading = 1
    else: 
        selected_AI_multithreading = int(selected_option.split()[0])

def select_gpu_from_menu(selected_option: str) -> None:
    global selected_gpu    
    selected_gpu = selected_option

def select_save_frame_from_menu(selected_option: str):
    global selected_keep_frames
    if   selected_option == "ON":  selected_keep_frames = True
    elif selected_option == "OFF": selected_keep_frames = False

def select_image_extension_from_menu(selected_option: str) -> None:
    global selected_image_extension   
    selected_image_extension = selected_option

def select_video_extension_from_menu(selected_option: str) -> None:
    global selected_video_extension   
    selected_video_extension = selected_option

def select_video_codec_from_menu(selected_option: str) -> None:
    global selected_video_codec
    selected_video_codec = selected_option




# GUI place functions ---------------------------

def place_loadFile_section() -> None:
    background = CTkFrame(master = window, fg_color = background_color, corner_radius = 1)

    text_drop = (" SUPPORTED FILES \n\n "
               + "VIDEOS • mp4 webm mkv flv gif avi mov mpg qt 3gp ")

    input_file_text = CTkLabel(
        master     = window, 
        text       = text_drop,
        fg_color   = background_color,
        bg_color   = background_color,
        text_color = text_color,
        width      = 300,
        height     = 150,
        font       = bold13,
        anchor     = "center"
    )
    
    input_file_button = CTkButton(
        master       = window,
        command      = open_files_action, 
        text         = "SELECT FILES",
        width        = 140,
        height       = 30,
        font         = bold12,
        border_width  = 1,
        corner_radius = 1,
        fg_color      = "#282828",
        text_color    = "#E0E0E0",
        border_color  = "#0096FF"
    )
    
    background.place(relx = 0.0, rely = 0.0, relwidth = 0.5, relheight = 1.0)
    input_file_text.place(relx = 0.25, rely = 0.4,  anchor = "center")
    input_file_button.place(relx = 0.25, rely = 0.5, anchor = "center")

def place_app_name() -> None:
    background = CTkFrame(master = window, fg_color = background_color)
    app_name_label = CTkLabel(
        master     = window, 
        text       = app_name + " " + version,
        fg_color   = background_color, 
        text_color = app_name_color,
        font       = bold18,
        anchor     = "w"
    )
    background.place(relx = 0.5, rely = 0.0, relwidth = 0.5, relheight = 1.0)
    app_name_label.place(relx = column_1 - 0.055, rely = row0, anchor = "center")

def place_app_zoom_and_links() -> None:

    # App zoom menu
    label_app_zoom = CTkLabel(
        master     = window,
        text       = "App zoom",
        width      = 50,
        height     = 22,
        fg_color   = "transparent",
        bg_color   = background_color,
        text_color = text_color,
        font       = bold13,
        anchor     = "w"
    )
    zoom_option_menu = create_option_menu(
        command       = select_app_zoom, 
        values        = zoom_option_list, 
        default_value = selected_app_zoom, 
        width         = 71
    )
    label_app_zoom.place(  relx = column_2-0.06,   rely = row0, anchor = "center")
    zoom_option_menu.place(relx = column_2+0.0155, rely = row0, anchor = "center")

    def opentelegram() -> None: open_browser(telegramme, new=1)
    def opengithub()   -> None: open_browser(githubme, new=1)

    # Telegram button
    telegram_button = create_link_button(command = opentelegram, icon = logo_telegram)
    telegram_button.place(relx = column_2+0.075, rely = row0, anchor = "center")

    # Github button
    git_button = create_link_button(command = opengithub, icon = logo_git)
    git_button.place(relx = column_2+0.11, rely = row0, anchor = "center")

def place_AI_menu() -> None:

    def open_info_AI_model():
        option_list = [
            "\n RIFE\n" + 
            "   • The complete RIFE AI model\n" + 
            "   • Excellent frame generation quality\n" + 
            "   • Recommended GPUs with VRAM >= 4GB\n",

            "\n RIFE_s (small)\n" + 
            "   • Lightweight version of RIFE AI model\n" +
            "   • High frame generation quality\n" +
            "   • 10% faster than full model\n" + 
            "   • Use less GPU VRAM memory\n" +
            "   • Recommended for GPUs with VRAM < 4GB \n",
        ]

        MessageBox(
            messageType   = "info",
            title         = "AI model",
            subtitle      = "This widget allows to choose between different AI models for frame generation",
            default_value = None,
            option_list   = option_list
        )


    widget_row = row1
    background = create_option_background()
    background.place(relx = 0.75, rely = widget_row, relwidth = 0.48, anchor = "center")
    
    info_button = create_info_button(open_info_AI_model, "AI model")
    option_menu = create_option_menu(select_AI_from_menu, AI_models_list, default_AI_model)

    info_button.place(relx = column_info1, rely = widget_row, anchor = "center")
    option_menu.place(relx = column_3_5,   rely = widget_row, anchor = "center")

def place_generation_option_menu() -> None:

    def open_info_frame_generation_option():
        option_list = [
            "\n FRAME GENERATION\n" + 
            "   • x2 - doubles video framerate • 30fps => 60fps\n" + 
            "   • x4 - quadruples video framerate • 30fps => 120fps\n" + 
            "   • x8 - octuplicate video framerate • 30fps => 240fps\n",

            "\n SLOWMOTION (no audio)\n" + 
            "   • Slowmotion x2 - slowmotion effect by a factor of 2\n" +
            "   • Slowmotion x4 - slowmotion effect by a factor of 4\n" +
            "   • Slowmotion x8 - slowmotion effect by a factor of 8\n"
        ]
        
        MessageBox(
            messageType   = "info",
            title         = "AI frame generation", 
            subtitle      = " This widget allows to choose between different AI frame generation option",
            default_value = None,
            option_list   = option_list
        )

    
    widget_row  = row2
    background = create_option_background()
    background.place(relx = 0.75, rely = widget_row, relwidth = 0.48, anchor = "center")

    info_button = create_info_button(open_info_frame_generation_option, "AI frame generation")
    option_menu = create_option_menu(select_framegeneration_option_from_menu, generation_options_list, default_generation_option)

    info_button.place(relx = column_info1, rely = widget_row, anchor = "center")
    option_menu.place(relx = column_3_5,   rely = widget_row, anchor = "center")

def place_AI_multithreading_menu() -> None:

    def open_info_AI_multithreading():
        option_list = [
            " This option can enhance video upscaling performance, especially on powerful GPUs.",

            " \n AI MULTITHREADING OPTIONS\n"
            + "  • OFF - Processes one frame at a time.\n"
            + "  • 2 threads - Processes two frames simultaneously.\n"
            + "  • 4 threads - Processes four frames simultaneously.\n"
            + "  • 6 threads - Processes six frames simultaneously.\n"
            + "  • 8 threads - Processes eight frames simultaneously.\n",

            " \n NOTES\n"
            + "  • Higher thread counts increase CPU, GPU, and RAM usage.\n"
            + "  • The GPU may be heavily stressed, potentially reaching high temperatures.\n"
            + "  • Monitor your system's temperature to prevent overheating.\n"
            + "  • If the chosen thread count exceeds GPU capacity, the app automatically selects an optimal value.\n",
        ]

        MessageBox(
            messageType   = "info",
            title         = "AI multithreading (EXPERIMENTAL)", 
            subtitle      = "This widget allows to choose how many video frames are upscaled simultaneously",
            default_value = None,
            option_list   = option_list
        )


    widget_row = row3
    background = create_option_background()
    background.place(relx = 0.75, rely = widget_row, relwidth = 0.48, anchor = "center")

    info_button = create_info_button(open_info_AI_multithreading, "AI multithreading")
    option_menu = create_option_menu(select_AI_multithreading_from_menu, AI_multithreading_list, default_AI_multithreading)

    info_button.place(relx = column_info1, rely = widget_row, anchor = "center")
    option_menu.place(relx = column_3_5,   rely = widget_row, anchor = "center")

def place_input_output_resolution_textboxs() -> None:

    def open_info_input_resolution():
        option_list = [
            " A high value (>50%) will create high quality video but will be slower",
            " While a low value (<50%) will create good quality videos but will much faster",

            " \n For example, for a 1080p (1920x1080) video\n" + 
            " • Input scale 25%  => input to AI 270p (480x270)\n" +
            " • Input scale 50%  => input to AI 540p (960x540)\n" + 
            " • Input scale 75%  => input to AI 810p (1440x810)\n" + 
            " • Input scale 100% => input to AI 1080p (1920x1080) \n",
        ]

        MessageBox(
            messageType   = "info",
            title         = "Input scale %",
            subtitle      = "This widget allows to choose the video resolution input to the AI",
            default_value = None,
            option_list   = option_list
        )

    def open_info_output_resolution():
        option_list = [
            " 100% maintains the exact resolution of the original input file",
            " A lower value (<100%) downscales the result relative to the original, ideal for reducing file size",
            " A higher value (>100%) upscales the output beyond the original resolution",

            "\n For example, if your original video is Full HD (1920x1080):\n" +
            " • Output scale 50%  => final output 960x540   (half size)\n" +
            " • Output scale 100% => final output 1920x1080 (original size)\n" +
            " • Output scale 200% => final output 3840x2160 (4K upscale)\n",
        ]

        MessageBox(
            messageType   = "info",
            title         = "Output scale %",
            subtitle      = "This widget allows to choose frame-generated video resolution",
            default_value = None,
            option_list   = option_list
        )


    widget_row = row4
    background = create_option_background()
    background.place(relx = 0.75, rely = widget_row, relwidth = 0.48, anchor = "center")

    # Input scale %%
    info_button = create_info_button(open_info_input_resolution, "Input scale %")
    option_menu = create_text_box(selected_input_resize_factor, width = little_textbox_width) 

    info_button.place(relx = column_info1, rely = widget_row, anchor = "center")
    option_menu.place(relx = column_1_5,   rely = widget_row, anchor = "center")

    # Output scale %
    info_button = create_info_button(open_info_output_resolution, "Output scale %")
    option_menu = create_text_box(selected_output_resize_factor, width = little_textbox_width)  

    info_button.place(relx = column_info2, rely = widget_row, anchor = "center")
    option_menu.place(relx = column_3,     rely = widget_row, anchor = "center")

def place_gpu_menu() -> None:

    def open_info_gpu():
        option_list = [
            "\n It is possible to select up to 4 GPUs for AI processing\n" +
            "  • Auto (the app will select the most powerful GPU)\n" + 
            "  • GPU 1 (GPU 0 in Task manager)\n" + 
            "  • GPU 2 (GPU 1 in Task manager)\n" + 
            "  • GPU 3 (GPU 2 in Task manager)\n" + 
            "  • GPU 4 (GPU 3 in Task manager)\n",

            "\n NOTES\n" +
            "  • Keep in mind that the more powerful the chosen gpu is, the faster the upscaling will be\n" +
            "  • For optimal performance, it is essential to regularly update your GPUs drivers\n" +
            "  • Selecting a GPU not present in the PC will cause the app to use the CPU for AI processing\n"
        ]

        MessageBox(
            messageType   = "info",
            title         = "GPU",
            subtitle      = "This widget allows to select the GPU for AI upscale",
            default_value = None,
            option_list   = option_list
        )


    widget_row = row5

    background  = create_option_background()
    background.place(relx = 0.75, rely = widget_row, relwidth = 0.48, anchor = "center")

    # GPU
    info_button = create_info_button(open_info_gpu, "GPU")
    option_menu = create_option_menu(select_gpu_from_menu, gpus_list, default_gpu, width = little_menu_width) 

    info_button.place(relx = column_info1,        rely = widget_row, anchor = "center")
    option_menu.place(relx = column_1_4, rely = widget_row,  anchor = "center")

def place_image_video_output_menus() -> None:

    def open_info_image_output():
        option_list = [
            " \n PNG\n"
            " • Very good quality\n"
            " • Slow and heavy file\n"
            " • Supports transparent images\n"
            " • Lossless compression (no quality loss)\n"
            " • Ideal for graphics, web images, and screenshots\n",

            " \n JPG\n"
            " • Good quality\n"
            " • Fast and lightweight file\n"
            " • Lossy compression (some quality loss)\n"
            " • Ideal for photos and web images\n"
            " • Does not support transparency\n",

            " \n BMP\n"
            " • Highest quality\n"
            " • Slow and heavy file\n"
            " • Uncompressed format (large file size)\n"
            " • Ideal for raw images and high-detail graphics\n"
            " • Does not support transparency\n",

            " \n TIFF\n"
            " • Highest quality\n"
            " • Very slow and heavy file\n"
            " • Supports both lossless and lossy compression\n"
            " • Often used in professional photography and printing\n"
            " • Supports multiple layers and transparency\n",
        ]


        MessageBox(
            messageType   = "info",
            title         = "Frame output",
            subtitle      = "This widget allows to choose the extension of generated frames",
            default_value = None,
            option_list   = option_list
        )

    def open_info_video_extension():
        option_list = [
            " \n MP4\n"
            " • Most widely supported format\n"
            " • Good quality with efficient compression\n"
            " • Fast and lightweight file\n"
            " • Ideal for streaming and general use\n",

            " \n MKV\n"
            " • High-quality format with multiple audio and subtitle tracks support\n"
            " • Larger file size compared to MP4\n"
            " • Supports almost any codec\n"
            " • Ideal for high-quality videos and archiving\n",

            " \n AVI\n"
            " • Older format with high compatibility\n"
            " • Larger file size due to less efficient compression\n"
            " • Supports multiple codecs but lacks modern features\n"
            " • Ideal for older devices and raw video storage\n",

            " \n MOV\n"
            " • High-quality format developed by Apple\n"
            " • Large file size due to less compression\n"
            " • Best suited for editing and high-quality playback\n"
            " • Compatible mainly with macOS and iOS devices\n",
        ]

        MessageBox(
            messageType   = "info",
            title         = "Video output",
            subtitle      = "This widget allows to choose the extension of the upscaled video",
            default_value = None,
            option_list   = option_list
        )

    widget_row = row6

    background = create_option_background()
    background.place(relx = 0.75, rely = widget_row, relwidth = 0.48, anchor = "center")

    # Image output
    info_button = create_info_button(open_info_image_output, "Frame output")
    option_menu = create_option_menu(select_image_extension_from_menu, image_extension_list, default_image_extension, width = little_menu_width)
    info_button.place(relx = column_info1,        rely = widget_row, anchor = "center")
    option_menu.place(relx = column_1_4, rely = widget_row, anchor = "center")

    # Video output
    info_button = create_info_button(open_info_video_extension, "Video output")
    option_menu = create_option_menu(select_video_extension_from_menu, video_extension_list, default_video_extension, width = little_menu_width)
    info_button.place(relx = column_info2,      rely = widget_row, anchor = "center")
    option_menu.place(relx = column_2_9, rely = widget_row, anchor = "center")

def place_video_codec_keep_frames_menus() -> None:

    def open_info_video_codec():
        option_list = [
            " \n SOFTWARE ENCODING (CPU)\n"
            " • x264 | H.264 software encoding\n"
            " • x265 | HEVC (H.265) software encoding\n",

            " \n NVIDIA GPU ENCODING (NVENC - Optimized for NVIDIA GPU)\n"
            " • h264_nvenc | H.264 hardware encoding\n"
            " • hevc_nvenc | HEVC (H.265) hardware encoding\n",

            " \n AMD GPU ENCODING (AMF - Optimized for AMD GPU)\n"
            " • h264_amf | H.264 hardware encoding\n"
            " • hevc_amf | HEVC (H.265) hardware encoding\n",

            " \n INTEL GPU ENCODING (QSV - Optimized for Intel GPU)\n"
            " • h264_qsv | H.264 hardware encoding\n"
            " • hevc_qsv | HEVC (H.265) hardware encoding\n"
        ]


        MessageBox(
            messageType   = "info",
            title         = "Video codec",
            subtitle      = "This widget allows to choose video codec for upscaled video",
            default_value = None,
            option_list   = option_list
        )

    def open_info_keep_frames():
        option_list = [
            "\n ON \n" + 
            " The app does NOT delete the video frames after creating the upscaled video \n",

            "\n OFF \n" + 
            " The app deletes the video frames after creating the upscaled video \n"
        ]

        MessageBox(
            messageType   = "info",
            title         = "Keep video frames",
            subtitle      = "This widget allows to choose to keep video frames",
            default_value = None,
            option_list   = option_list
        )


    widget_row = row7

    background = create_option_background()
    background.place(relx = 0.75, rely = widget_row, relwidth = 0.48, anchor = "center")

    # Video codec
    info_button = create_info_button(open_info_video_codec, "Video codec")
    option_menu = create_option_menu(select_video_codec_from_menu, video_codec_list, default_video_codec, width = little_menu_width)
    info_button.place(relx = column_info1,        rely = widget_row, anchor = "center")
    option_menu.place(relx = column_1_4, rely = widget_row, anchor = "center")

    # Keep frames
    info_button = create_info_button(open_info_keep_frames, "Keep frames")
    option_menu = create_option_menu(select_save_frame_from_menu, keep_frames_list, default_keep_frames, width = little_menu_width)
    info_button.place(relx = column_info2,      rely = widget_row, anchor = "center")
    option_menu.place(relx = column_2_9, rely = widget_row, anchor = "center")

def place_output_path_textbox() -> None:

    def open_info_output_path():
        option_list = [
              "\n The default path is defined by the input files."
            + "\n For example: selecting a file from the Download folder,"
            + "\n the app will save upscaled files in the Download folder \n",

            " Otherwise it is possible to select the desired path using the SELECT button",
        ]

        MessageBox(
            messageType   = "info",
            title         = "Output path",
            subtitle      = "This widget allows to choose upscaled files path",
            default_value = None,
            option_list   = option_list
        )

    background    = create_option_background()
    info_button   = create_info_button(open_info_output_path, "Output path")
    option_menu   = create_text_box_output_path(selected_output_path) 
    active_button = create_active_button(
        command = open_output_path_action, 
        text    = "SELECT", 
        icon    = None, 
        width   = 60, 
        height  = 25
    )
  
    background.place(   relx = 0.75,                 rely = row10, relwidth = 0.48,  anchor = "center")
    info_button.place(  relx = column_info1,         rely = row10 - 0.003,           anchor = "center")
    active_button.place(relx = column_info1 + 0.052, rely = row10,                   anchor = "center")
    option_menu.place(  relx = column_2 - 0.008,     rely = row10,                   anchor = "center")

def place_message_label() -> None:
    message_label = CTkLabel(
        master        = window, 
        textvariable  = info_message,
        height        = 24,
        width         = 247,
        font          = bold11,
        fg_color      = "#ffbf00",
        text_color    = "#000000",
        anchor        = "center",
        corner_radius = 1
    )
    message_label.place(relx = 0.85, rely = 0.9495, anchor = "center")

def place_stop_button() -> None: 
    stop_button = create_active_button(
        command      = stop_button_command,
        text         = "STOP",
        icon         = stop_icon,
        width        = 140,
        height       = 30,
        border_color = "#EC1D1D"
    )
    stop_button.place(relx = 0.75 - 0.1, rely = 0.95, anchor = "center")

def place_generation_button() -> None: 
    generation_button = create_active_button(
        command = generate_button_command,
        text    = "GENERATE",
        icon    = play_icon,
        width   = 140,
        height  = 30
    )
    generation_button.place(relx = 0.75 - 0.1, rely = 0.95, anchor = "center")




# App related functions ---------------------------

def save_user_choices_in_json() -> None:
    global selected_app_zoom
    global selected_AI_model
    global selected_generation_option
    global selected_gpu
    global selected_AI_multithreading
    global selected_keep_frames
    global selected_image_extension
    global selected_video_extension
    global selected_video_codec

    app_zoom_to_save           = selected_app_zoom
    AI_model_to_save           = selected_AI_model
    generation_options_to_save = selected_generation_option
    gpu_to_save                = selected_gpu
    image_extension_to_save    = selected_image_extension
    video_extension_to_save    = selected_video_extension
    video_codec_to_save        = selected_video_codec

    keep_frames_to_save = "OFF"
    if selected_keep_frames == True: keep_frames_to_save = "ON"

    if selected_AI_multithreading == 1: AI_multithreading_to_save = "OFF"
    else: AI_multithreading_to_save = f"{selected_AI_multithreading} threads"

    user_preference = {
        "default_app_zoom":             app_zoom_to_save,
        "default_AI_model":             AI_model_to_save,
        "default_generation_option":    generation_options_to_save,
        "default_AI_multithreading":    AI_multithreading_to_save,
        "default_gpu":                  gpu_to_save,
        "default_keep_frames":          keep_frames_to_save,
        "default_image_extension":      image_extension_to_save,
        "default_video_extension":      video_extension_to_save,
        "default_video_codec":          video_codec_to_save,
        "default_output_path":          selected_output_path.get(),
        "default_input_resize_factor":  str(selected_input_resize_factor.get()),
        "default_output_resize_factor": str(selected_output_resize_factor.get()),
    }
    user_preference_json = json_dumps(user_preference)
    with open(USER_PREFERENCE_PATH, "w") as preference_file:
        preference_file.write(user_preference_json)

def on_app_close():
    # 1. Save user choices in file
    save_user_choices_in_json()

    # 2. Destroy app window
    window.grab_release()
    window.destroy()

    # 3. Stop frame-generation process and thread check_frame-generation_step
    write_process_status(process_status_q, f"{CLOSE_APP_STATUS}")
    stop_framegeneration_process()

class App():
    def __init__(self, window) -> None:
        self.toplevel_window = None
        window.protocol("WM_DELETE_WINDOW", on_app_close)

        window.title('')
        window.geometry("1000x675")
        window.resizable(False, False)
        window.iconbitmap(find_by_relative_path("Assets" + os_separator + "logo.ico"))

        place_loadFile_section()

        place_app_name()
        place_app_zoom_and_links()

        place_AI_menu()
        place_generation_option_menu()
        place_AI_multithreading_menu()
        place_input_output_resolution_textboxs()
        place_gpu_menu()
        place_image_video_output_menus()
        place_video_codec_keep_frames_menus()

        place_message_label()
        place_generation_button()
        place_output_path_textbox()



# Main functions ---------------------------

if __name__ == "__main__":

    if os_path_exists(USER_PREFERENCE_PATH):
        print(f"[{app_name}] Preference file exist")
        with open(USER_PREFERENCE_PATH, "r") as json_file:
            json_data = json_load(json_file)
            default_app_zoom             = json_data.get("default_app_zoom",             "100%")
            default_AI_model             = json_data.get("default_AI_model",             AI_models_list[0])
            default_AI_multithreading    = json_data.get("default_AI_multithreading",    AI_multithreading_list[0])
            default_generation_option    = json_data.get("default_generation_option",    generation_options_list[0])
            default_gpu                  = json_data.get("default_gpu",                  gpus_list[0])
            default_keep_frames          = json_data.get("default_keep_frames",          keep_frames_list[0])
            default_image_extension      = json_data.get("default_image_extension",      image_extension_list[0])
            default_video_extension      = json_data.get("default_video_extension",      video_extension_list[0])
            default_video_codec          = json_data.get("default_video_codec",          video_codec_list[0])
            default_output_path          = json_data.get("default_output_path",          OUTPUT_PATH_CODED)
            default_input_resize_factor  = json_data.get("default_input_resize_factor",  str(50))
            default_output_resize_factor = json_data.get("default_output_resize_factor", str(100))
    else:
        print(f"[{app_name}] Preference file does not exist, using default coded value")
        default_app_zoom             = "100%"
        default_AI_model             = AI_models_list[0]
        default_AI_multithreading    = AI_multithreading_list[0]
        default_generation_option    = generation_options_list[0]
        default_gpu                  = gpus_list[0]
        default_image_extension      = image_extension_list[0]
        default_video_extension      = video_extension_list[0]
        default_video_codec          = video_codec_list[0]
        default_keep_frames          = keep_frames_list[0]
        default_output_path          = OUTPUT_PATH_CODED
        default_input_resize_factor  = str(50)
        default_output_resize_factor = str(100)

    multiprocessing_freeze_support()
    set_appearance_mode("Dark")
    set_default_color_theme("dark-blue")
    apply_app_zoom(float(default_app_zoom.replace("%", "")) / 100)

    # Get total RAM of the PC
    free_ram_gb   = psutil_virtual_memory().available / (1024**3)
    queue_maxsize = max(50, int(free_ram_gb * 30))
    print(f"[__main__] free RAM: {free_ram_gb:.2f} GB - queue_maxsize = {queue_maxsize}")
    
    # Multiprocessing utilities
    multiprocessing_manager            = multiprocessing_Manager()
    process_status_q                   = multiprocessing_manager.Queue(maxsize=1)
    video_frames_and_info_q            = multiprocessing_manager.Queue(maxsize=queue_maxsize)
    event_stop_framegeneration_process = multiprocessing_manager.Event()

    window = CTk() 
    info_message                  = StringVar()
    selected_output_path          = StringVar()
    selected_input_resize_factor  = StringVar()
    selected_output_resize_factor = StringVar()

    global selected_app_zoom
    global selected_file_list
    global selected_AI_model
    global selected_generation_option
    global selected_AI_multithreading
    global selected_gpu 
    global selected_keep_frames
    global selected_image_extension
    global selected_video_extension
    global selected_video_codec

    selected_app_zoom          = default_app_zoom
    selected_file_list         = []
    selected_AI_model          = default_AI_model
    selected_generation_option = default_generation_option
    selected_gpu               = default_gpu
    selected_image_extension   = default_image_extension
    selected_video_extension   = default_video_extension
    selected_video_codec       = default_video_codec

    if default_AI_multithreading == "OFF": 
        selected_AI_multithreading = 1
    else:                                  
        selected_AI_multithreading = int(default_AI_multithreading.split()[0])

    selected_keep_frames = False
    if default_keep_frames == "ON": selected_keep_frames = True

    selected_input_resize_factor.set(default_input_resize_factor)
    selected_output_resize_factor.set(default_output_resize_factor)
    selected_output_path.set(default_output_path)

    info_message.set("Hi :)")
    selected_input_resize_factor.trace_add('write', update_file_widget)
    selected_output_resize_factor.trace_add('write', update_file_widget)

    font   = "Segoe UI"    
    bold8  = CTkFont(family = font, size = 8, weight = "bold")
    bold9  = CTkFont(family = font, size = 9, weight = "bold")
    bold10 = CTkFont(family = font, size = 10, weight = "bold")
    bold11 = CTkFont(family = font, size = 11, weight = "bold")
    bold12 = CTkFont(family = font, size = 12, weight = "bold")
    bold13 = CTkFont(family = font, size = 13, weight = "bold")
    bold14 = CTkFont(family = font, size = 14, weight = "bold")
    bold16 = CTkFont(family = font, size = 16, weight = "bold")
    bold17 = CTkFont(family = font, size = 17, weight = "bold")
    bold18 = CTkFont(family = font, size = 18, weight = "bold")
    bold19 = CTkFont(family = font, size = 19, weight = "bold")
    bold20 = CTkFont(family = font, size = 20, weight = "bold")
    bold21 = CTkFont(family = font, size = 21, weight = "bold")
    bold22 = CTkFont(family = font, size = 22, weight = "bold")
    bold23 = CTkFont(family = font, size = 23, weight = "bold")
    bold24 = CTkFont(family = font, size = 24, weight = "bold")

    # Images
    logo_git      = CTkImage(pillow_image_open(find_by_relative_path(f"Assets{os_separator}github_logo.png")),    size=(18, 18))
    logo_telegram = CTkImage(pillow_image_open(find_by_relative_path(f"Assets{os_separator}telegram_logo.png")),  size=(16, 16))
    stop_icon     = CTkImage(pillow_image_open(find_by_relative_path(f"Assets{os_separator}stop_icon.png")),      size=(15, 15))
    play_icon     = CTkImage(pillow_image_open(find_by_relative_path(f"Assets{os_separator}upscale_icon.png")),   size=(15, 15))
    clear_icon    = CTkImage(pillow_image_open(find_by_relative_path(f"Assets{os_separator}clear_icon.png")),     size=(15, 15))
    info_icon     = CTkImage(pillow_image_open(find_by_relative_path(f"Assets{os_separator}info_icon.png")),      size=(18, 18))

    app = App(window)
    window.update()
    window.mainloop()