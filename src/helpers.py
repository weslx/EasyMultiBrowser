import random
import time

def automation_flow(sb):
    # Random delay to avoid patterns
    sb.sleep(random.uniform(1, 3))
    
    # Navigate to the site
    sb.open("https://hailuoaifree.com/image-to-video")
    sb.sleep(random.uniform(1.5, 3))
    
    for _ in range(2):
        sb.execute_script(f"window.scrollTo(0, {random.randint(100, 300)});")
        sb.sleep(random.uniform(0.5, 1.2))
    
    try:
        # Click the Mine button
        mine_button = "#gallery > div.flex.gap-8.mb-8.border-b.border-surface-border > h2:nth-child(2) > button"
        sb.wait_for_element(mine_button)
        sb.click(mine_button)
        print("✅ Mine button clicked successfully")
        
        sb.sleep(random.uniform(2, 3))
        
        # Monitor for completion and download
        success = download_videos(sb)
        return success
        
    except Exception as e:
        print(f"⚠️ Error during automation flow: {str(e)}")
        return False

def download_videos(sb):
    """Download os 2 primeiros vídeos disponíveis"""
    try:
        # Encontrar todos os vídeos e seus botões de download
        videos_info = sb.execute_script("""
            // Encontrar todos os vídeos
            const videos = Array.from(document.querySelectorAll('video.w-full.h-full.object-contain'));
            const results = [];
            
            // Para cada vídeo, buscar seu botão de download correspondente
            for (const video of videos) {
                // Ir subindo até encontrar o card que contém o vídeo
                const container = video.closest('.bg-surface-light.rounded-2xl');
                if (!container) continue;
                
                // Pular se for anúncio
                if (container.closest('.adsbygoogle')) continue;
                
                // Encontrar o botão de download
                const downloadBtn = container.querySelector('a[download]');
                if (downloadBtn) {
                    results.push({
                        videoSrc: video.src,
                        downloadUrl: downloadBtn.href,
                        downloadBtn: downloadBtn  // Referência ao elemento
                    });
                }
            }
            
            return results;
        """)
        
        print(f"Found {len(videos_info)} videos with download buttons")
        
        # Baixar os 2 primeiros vídeos
        download_count = 0
        for i, video in enumerate(videos_info[:2]):
            try:
                print(f"Downloading video {i+1}: {video['videoSrc']}")
                # Clicar no botão de download
                sb.execute_script("arguments[0].click();", sb.execute_script(f"""
                    return document.querySelector('a[href="{video['downloadUrl']}"][download]');
                """))
                download_count += 1
                # Pequena pausa entre downloads
                sb.sleep(1)
            except Exception as e:
                print(f"⚠️ Error downloading video {i+1}: {e}")
        
        print(f"✅ Downloaded {download_count} videos")
        return download_count > 0
        
    except Exception as e:
        print(f"⚠️ Error in download_videos: {e}")
        return False