# Browse Content Library — Task Workflow

## Objective

Browse DropKick's content library on Google Drive to find available photos and videos for social media posts, campaigns, and content kits.

## Content Library Location

**Shared Drive:** DropKick content drive
**Root Folder:** `11-dmJwvkPaQVFhoWcBsGSsdkY98TxCKr` (Anderson Lock & Safe)
**Drive ID:** `0AO4AqX6zFb6DUk9PVA`

## Folder Structure

Content is organized by month:
```
Anderson Lock & Safe/
├── August 2024/
├── September 2024/
├── ...
├── March 2026/
│   ├── Content 1.mp4
│   ├── Content 2.mp4
│   ├── Content 3.mp4
│   ├── Content 4.mp4
│   ├── Content 5.mp4
│   ├── DSC00096.jpg
│   ├── DSC00101.jpg
│   ├── DSC00102.jpg
│   └── Raw Footage/
├── April 2026/
│   └── Raw Footage/
├── [Brand Assets]/
└── [Customer Docs]/
```

Each month folder typically contains:
- **Finished videos** (Content 1.mp4, Content 2.mp4, etc.) — edited, ready to post
- **Photos** (DSC*.jpg) — professional shots from the shoot
- **Raw Footage/** subfolder — unedited footage for repurposing

## Tool

**Google Workspace MCP** — `gws_run` with service `drive`

All requests require these params:
```
supportsAllDrives: "true"
includeItemsFromAllDrives: "true"
corpora: "allDrives"
```

## Steps

### 1. List Available Months

```
GET files
  q: '11-dmJwvkPaQVFhoWcBsGSsdkY98TxCKr' in parents
  fields: files(id,name,mimeType,modifiedTime)
  pageSize: 50
```

### 2. Browse a Month's Content

```
GET files
  q: '<month_folder_id>' in parents
  fields: files(id,name,mimeType,size,modifiedTime)
  pageSize: 50
```

### 3. Get File Details (for posting)

For each file you want to use:
```
GET files/<file_id>
  fields: id,name,mimeType,thumbnailLink,webViewLink,webContentLink,videoMediaMetadata,imageMediaMetadata
```

This returns:
- **`thumbnailLink`** — Preview image (viewable by the agent)
- **`webContentLink`** — Direct download URL (use for Buffer media attachments)
- **`webViewLink`** — Shareable link (for humans / ClickUp task references)
- **`videoMediaMetadata`** — Width, height, duration in milliseconds
- **`imageMediaMetadata`** — Width, height, camera info

### 4. View an Image

To actually look at a photo and make creative decisions:
```
GET files/<file_id>
  fields: thumbnailLink,webContentLink
```
Then view the image at the thumbnailLink URL.

### 5. Preview a Video

Videos can't be watched directly. Instead:
- View the `thumbnailLink` to see a frame
- Check `videoMediaMetadata` for dimensions and duration
- Vertical (1080x1920) = Reel/Story format
- Horizontal (1920x1080) = Feed/YouTube format
- Duration under 60s = Reel-ready
- Duration over 60s = May need trimming or is long-form

## Using Content for Buffer Posts

When scheduling a post with media via `tools/buffer_publish.py`, the `webContentLink` from Google Drive can be used as the asset URL. The file must have link sharing enabled.

## Content Naming Conventions

- `Content X.mp4` — Finished, edited video from DropKick (X = sequence number)
- `DSC*.jpg` — Professional photos from the shoot
- `Raw Footage/` — Unedited footage, typically larger files
- `[Brand Assets]/` — Logos, templates, brand materials
- `[Customer Docs]/` — Customer-related documents

## Edge Cases

- **Empty month folders** — Future months may only have an empty Raw Footage subfolder. This means DropKick hasn't delivered content yet.
- **Raw footage** — Available for repurposing but requires editing. Note in task if raw footage is being recommended.
- **File sharing permissions** — If `webContentLink` returns a 403 when used in Buffer, the file may need its sharing settings updated. Flag for Garrett.
- **Large files** — Videos can be 50-100MB+. Don't try to download them locally. Use the URLs.
