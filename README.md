# 时光留声 - 部署指南

## 项目概述
"时光留声"是一个基于Supabase和Vercel的Web应用，支持用户注册登录、音视频录制、遗物创建和管理，数据持久化存储在云端。

## 技术栈
- **后端**：Supabase（认证 + 数据库 + 存储）
- **前端**：原生HTML/JS/CSS + Supabase JS SDK
- **部署**：Vercel（前端）+ Supabase（云后端）

## 部署步骤

### 1. 创建Supabase项目
1. 访问 [Supabase官网](https://supabase.com/) 并注册登录
2. 点击「New Project」创建新项目
3. 填写项目名称、选择Region，设置数据库密码
4. 等待项目创建完成

### 2. 配置Supabase认证
1. 在Supabase控制台中，点击左侧导航栏的「Authentication」
2. 点击「Settings」选项卡
3. 在「Site URL」中输入您的Vercel部署域名（稍后会获得）
4. 在「Additional redirect URLs」中添加 `http://localhost:3000`（用于本地开发）
5. 保存设置

### 3. 创建数据库表
在Supabase控制台中，点击左侧导航栏的「SQL Editor」，执行以下SQL语句创建表结构：

```sql
-- 创建联系人表
CREATE TABLE contacts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id),
  name TEXT NOT NULL,
  email TEXT,
  phone TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- 创建遗物表
CREATE TABLE relics (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id),
  contact_id UUID REFERENCES contacts(id),
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  ai_enhanced_content TEXT,
  audio_url TEXT,
  video_url TEXT,
  silence_threshold_days INTEGER DEFAULT 7,
  created_at TIMESTAMP DEFAULT NOW()
);

-- 创建录制文件表
CREATE TABLE recording_files (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id),
  relic_id UUID REFERENCES relics(id),
  file_url TEXT NOT NULL,
  file_type TEXT NOT NULL,
  duration INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

-- 启用行级安全策略
ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE relics ENABLE ROW LEVEL SECURITY;
ALTER TABLE recording_files ENABLE ROW LEVEL SECURITY;

-- 创建行级安全策略
CREATE POLICY "Users can view their own contacts" ON contacts
  FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can create their own contacts" ON contacts
  FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update their own contacts" ON contacts
  FOR UPDATE USING (user_id = auth.uid());

CREATE POLICY "Users can delete their own contacts" ON contacts
  FOR DELETE USING (user_id = auth.uid());

CREATE POLICY "Users can view their own relics" ON relics
  FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can create their own relics" ON relics
  FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update their own relics" ON relics
  FOR UPDATE USING (user_id = auth.uid());

CREATE POLICY "Users can delete their own relics" ON relics
  FOR DELETE USING (user_id = auth.uid());

CREATE POLICY "Users can view their own recording files" ON recording_files
  FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can create their own recording files" ON recording_files
  FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update their own recording files" ON recording_files
  FOR UPDATE USING (user_id = auth.uid());

CREATE POLICY "Users can delete their own recording files" ON recording_files
  FOR DELETE USING (user_id = auth.uid());
```

### 4. 创建Supabase存储桶
1. 在Supabase控制台中，点击左侧导航栏的「Storage」
2. 点击「New Bucket」创建新存储桶
3. 输入存储桶名称：`recordings`
4. 取消勾选「Public Bucket」选项
5. 点击「Create Bucket」

### 5. 配置存储桶访问权限
1. 在存储桶列表中，点击 `recordings` 存储桶
2. 点击「Policies」选项卡
3. 点击「New Policy」创建新策略
4. 选择「Only authenticated users can upload files」模板
5. 点击「Use this template」
6. 修改策略名称为「Users can upload their own files」
7. 在「Conditions」中添加：`bucket_id = 'recordings'`
8. 点击「Review」然后「Save Policy」

### 6. 获取Supabase配置信息
1. 在Supabase控制台中，点击左侧导航栏的「Settings」
2. 点击「API」选项卡
3. 复制「Project URL」和「anon key」

### 7. 部署前端到Vercel
1. 访问 [Vercel官网](https://vercel.com/) 并注册登录
2. 点击「New Project」创建新项目
3. 选择「Import Git Repository」或「Upload」上传项目文件
4. 填写项目名称，选择Region
5. 在「Environment Variables」中添加以下环境变量：
   - `VITE_SUPABASE_URL`：填写您的Supabase Project URL
   - `VITE_SUPABASE_ANON_KEY`：填写您的Supabase anon key
6. 点击「Deploy」部署项目
7. 等待部署完成，获取部署域名

### 8. 更新前端代码中的Supabase配置
1. 在 `index.html` 和 `app.html` 文件中，找到以下代码：
   ```javascript
   // Supabase配置
   const supabaseUrl = 'YOUR_SUPABASE_URL';
   const supabaseAnonKey = 'YOUR_SUPABASE_ANON_KEY';
   ```
2. 将 `YOUR_SUPABASE_URL` 和 `YOUR_SUPABASE_ANON_KEY` 替换为您的实际配置信息
3. 重新部署到Vercel

### 9. 本地开发
1. 克隆项目到本地
2. 使用 `python -m http.server 8000` 启动本地HTTP服务器
3. 打开浏览器，访问 `http://localhost:8000`

## 核心功能
1. **用户系统**：注册/登录，密码加密存储
2. **音视频录制**：实时预览，录制后自动上传
3. **数据持久化**：所有数据存入Supabase，跨设备可见
4. **遗物管理**：为指定联系人创建遗物，支持文字输入和AI润色
5. **沉默阈值**：用户可为遗物设置N天沉默阈值

## 注意事项
1. 音视频录制功能需要用户授权摄像头和麦克风权限
2. 录制的文件会上传到Supabase Storage，请注意存储空间限制
3. 沉默阈值功能在当前版本中为演示模式，实际触发需要后端定时任务支持
4. AI润色功能在当前版本中为模拟实现，实际应用中可以接入真实的AI API

## 故障排除
1. **无法登录**：检查Supabase认证配置中的Site URL是否正确
2. **无法上传文件**：检查存储桶权限配置是否正确
3. **无法加载联系人/遗物**：检查数据库表的行级安全策略是否正确配置
4. **音视频录制失败**：检查浏览器是否支持MediaRecorder API，是否已授权摄像头和麦克风权限

## 联系我们
如有任何问题或建议，请联系项目维护者。