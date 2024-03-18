import re, os

def merge_subtitle_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    merged_lines = []
    buffer = []
    for line in lines:
        # 如果是序号行，则开始新的字幕块
        if re.match(r'^\d+$', line):
            if buffer:
                merged_lines.append(' '.join(buffer))
                buffer = []
            merged_lines.append(line)  # 添加序号行
        # 如果是时间戳行，添加到merged_lines并清空buffer
        elif re.match(r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$', line):
            if buffer:
                merged_lines.append(' '.join(buffer))
                buffer = []
            merged_lines.append(line)  # 添加时间戳行
        # 如果是空行，添加到merged_lines并清空buffer
        elif line.strip() == '':
            if buffer:
                merged_lines.append(' '.join(buffer))
                buffer = []
            merged_lines.append(line)  # 添加空行
        # 将字幕内容行添加到缓冲区
        elif line.strip():
            buffer.append(line.strip())
    # 添加最后一个字幕块
    if buffer:
        merged_lines.append(' '.join(buffer))
    return merged_lines
def rewrite_subtitle_file(file_path, merged_lines):
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in merged_lines:
            file.write(line)

def srcFormat(file_path, saveDir=""):
    """
       字幕文件格式化。
       参数:
       * file_path -- 字幕文件路径。
       saveDir -- 格式化后的保存路径。
    """
    # 使用函数
    merged_lines = merge_subtitle_content(file_path)
    normalized_path = os.path.normpath(file_path)
    title = os.path.basename(normalized_path);
    if saveDir:
        tfile_path = os.path.join(saveDir, f"update_{title}");
    else:
        originPath = os.path.dirname(file_path);
        tfile_path = os.path.join(originPath, f"update_{title}");
    rewrite_subtitle_file(tfile_path, merged_lines)
# if __name__ == '__main__':
#     # 使用函数
#     file_path = r'E:\AutoMedia\发布视频\睡前故事\3月16日\3月16日.srt'  # 替换为你的字幕文件路径
#     merged_lines = merge_subtitle_content(file_path)
#     tfile_path = r'E:\AutoMedia\发布视频\睡前故事\3月16日\_update.srt'  # 替换为你的字幕文件路径
#     rewrite_subtitle_file(tfile_path, merged_lines)
