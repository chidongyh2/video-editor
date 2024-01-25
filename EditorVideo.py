import subprocess
import re, json, random, time
import moviepy.editor as mp
def flip_video(input_file, output_file):
    print("đang xử lý video...")
    zoom_factor = 1.09  # Increase to zoom in, decrease to zoom out
    x_percent, y_percent = 2, 3  
    width_percent, height_percent = 98, 97
    bitrate = random.randrange(800, 1200)
    start_time = 0.8  # Start time in seconds
    duration = mp.VideoFileClip(input_file).duration
    cmd = []
    if duration is not None:
        cmd = [
            'ffmpeg',
            '-i', input_file,  # Input file path
            '-vf', f'crop=iw*{width_percent/100}:ih*{height_percent/100}:iw*{x_percent/100}:ih*{y_percent/100},hflip',    # Horizontal flip filter
            '-b:v', f'{bitrate/2}k',
            '-y',
            '-ss', "0.8",  # Start time in seconds
            '-to', f"{duration - 1}",    # End time in seconds
            '-c:a', 'copy',    # Copy audio codec
            output_file # Output file path
        ]
    else:
        cmd = [
            'ffmpeg',
            '-i', input_file,  # Input file path
            '-vf', f'crop=iw*{width_percent/100}:ih*{height_percent/100}:iw*{x_percent/100}:ih*{y_percent/100},hflip',    # Horizontal flip filter
            '-b:v', f'{bitrate/2}k',
            '-y',
            '-ss', "0.8",  # Start time in seconds
            '-c:a', 'copy',    # Copy audio codec
            output_file # Output file path
        ]
    # Run FFmpeg command
    subprocess.run(cmd)
    
def chen_video(input_file, background_file, output_file):
    print("đang xử lý video...")
    volume_factor = 0.7  # Giảm âm lượng 50%
    speed_factor = 1.1  # Tăng tốc độ video gấp đôi. khi tăng thời gian video sẽ được kéo dài ra và âm lượng sẽ bị mất
    brightness_factor = 0.1  # Giảm độ sáng 10%
    brightness_factor_background = 0.1 # Giảm độ sáng 10%
    cmd_get_info = ['ffprobe', '-v', 'error', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', background_file]
    result = subprocess.run(cmd_get_info, stdout=subprocess.PIPE, text=True)
    width, height = map(int, result.stdout.strip().split(','))
    new_width2 = 426/720 * 4/3 * height
    new_height2 = 3/4 * height
    # Xác định kích thước của video được chèn và tính toán vị trí để đặt video vào trung tâm
    cmd_get_info_chen = ['ffprobe', '-v', 'error', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', input_file]
    result_chen = subprocess.run(cmd_get_info_chen, stdout=subprocess.PIPE, text=True)
    width_chen, height_chen = map(int, result_chen.stdout.strip().split(','))
    new_width = 853/720 * 4/3 * height_chen
    new_height =  3/4 * height_chen
    crop_x = (width_chen - new_width) // 2
    crop_y = (height_chen - new_height) // 2
    print(new_width, new_height, crop_x, crop_y)
    # Xác định thời lượng của video chèn
    cmd_get_duration = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', input_file]
    result_duration = subprocess.run(cmd_get_duration, stdout=subprocess.PIPE, text=True)
    duration_source = float(result_duration.stdout.strip())

    # Xác định thời lượng của video chèn
    cmd_get_duration = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', background_file]
    result_duration = subprocess.run(cmd_get_duration, stdout=subprocess.PIPE, text=True)
    duration_chen = float(result_duration.stdout.strip())

    filtergraph = (
        f'[1:v]scale=720:1280,eq=brightness={brightness_factor},setpts={speed_factor}*PTS[chen];'
        f'[2:v]crop={new_width2}:{new_height2}:(in_w-{new_width2})/2:(in_h-{new_height2})/2,scale=720:426,eq=brightness={brightness_factor_background},format=yuva420p,colorchannelmixer=aa=0.5,setpts={speed_factor}*PTS[video_to_add];'
        f'[0:v]crop={new_width}:{new_height}:(in_w-{new_width})/2:(in_h-{new_height})/2, scale=720:853, eq=brightness={brightness_factor},[chen]overlay=0:0[outv];'
        f'[outv][video_to_add]overlay=0:853[final_outv]'
    )
    if duration_source > duration_chen:
        filtergraph = (
        f'[1:v]scale=720:1280,eq=brightness={brightness_factor},setpts={speed_factor}*PTS[chen];'
        f'[2:v]loop={(duration_source - duration_chen)/duration_chen}:32767:0,crop={new_width2}:{new_height2}:(in_w-{new_width2})/2:(in_h-{new_height2})/2,scale=720:426,eq=brightness={brightness_factor_background},format=yuva420p,colorchannelmixer=aa=0.5,setpts={speed_factor}*PTS[video_to_add];'
        f'[0:v]crop={new_width}:{new_height}:(in_w-{new_width})/2:(in_h-{new_height})/2, scale=720:853, eq=brightness={brightness_factor},[chen]overlay=0:0[outv];'
        f'[outv][video_to_add]overlay=0:853[final_outv]'
    )    
    #,scale=320:384:flags=lanczos
    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-i', input_file,
        '-i', background_file,
        '-filter_complex', filtergraph,
        '-map', '[final_outv]',
        '-map', '0:a:0?',  # Chọn luồng âm thanh từ video chèn
        '-c:a', 'aac',  # Chuyển đổi âm thanh sang định dạng AAC
        '-b:a', '192k',  # Đặt tốc độ bit âm thanh
        '-af', f'volume={volume_factor}',  # Bộ lọc giảm âm lượng
        '-c:v', 'libx264',
        '-crf', '18',
        '-y',
        '-preset', 'veryfast',
        output_file
    ]
    # Run FFmpeg command
    subprocess.run(cmd, check=True)
    
def convert_to_grayscale(input_video, output_video_grayscale):
    # Xây dựng lệnh FFmpeg với bộ lọc chuyển đổi thành đen trắng
    cmd = [
        'ffmpeg',
        '-i', input_video,
        '-vf', 'colorchannelmixer=.3:.4:.3:0:.3:.4:.3:0:.3:.4:.3',  # Bộ lọc chuyển đổi thành đen trắng
        '-c:v', 'libx264',
        '-crf', '18',
        '-preset', 'veryfast',
        output_video_grayscale
    ]

    # Chạy lệnh FFmpeg
    subprocess.run(cmd, check=True) 
    
if __name__ == '__main__':
    #edit_video("videos/hehe.mp4", "hehe_save.mp4", cuts)
    #flip_video("videos/hehe.mp4", "hehe_save.mp4")
    chen_video("video-sources/lebaobinh.mp4", "video-sources/background.mp4", "hehe_save.mp4")
    #convert_to_grayscale("videos/waves.mp4", "videos/background.mp4")