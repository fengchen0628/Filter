import os
import glob
import yaml

def parse_list_file(file_path):
    rules = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 过滤空行与注释（以 # 或 // 开头的行）
            if not line or line.startswith('#') or line.startswith('//'):
                continue
            rules.append(line)
    return rules

def main():
    # 假设所有的 .list 文件都在 rules/ 目录下
    input_dir = "rules"
    output_dir = "generated"

    os.makedirs(output_dir, exist_ok=True)

    # 扫描所有的 .list 文件
    list_files = glob.glob(os.path.join(input_dir, "*.list"))

    for list_file in list_files:
        filename = os.path.basename(list_file)
        name_without_ext = os.path.splitext(filename)[0]
        
        # 解析规则条目
        rules = parse_list_file(list_file)

        # 构建 Clash / Mihomo Rule-Provider 要求的 YAML 结构
        yaml_data = {
            'payload': rules
        }

        output_path = os.path.join(output_dir, f"{name_without_ext}.yaml")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            # 写入 YAML，保持列表缩进样式
            yaml.dump(yaml_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            
        print(f"成功转换: {list_file} -> {output_path}")

if __name__ == "__main__":
    main()
